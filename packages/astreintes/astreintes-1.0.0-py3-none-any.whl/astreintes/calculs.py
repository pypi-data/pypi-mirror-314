import numpy as np
import pandas as pd
import logging

import astreintes.models as models
from astreintes.models import N_SEMAINES

_logger = logging.getLogger(__name__)


def _repartition(p, n_semaines=N_SEMAINES, max_astreintes=13):
    """
    Calcule la répartition d'un nombre entier (en général semaines) en len(p) personnes,
    avec un maximum (13 par défaut) et des affinités (vecteur p).
    :param p: préférence pour chaque technicien ou site
    :param n_semaines: nombre de semaines à répartir, 52 semaines par an par default
    :param max_astreintes: 13 semaines maximum par technicien par défault,
    peut-être un scalaire ou un vecteur size(p)
    :return:
    """
    p = p / p.sum()  # on normalise les probabilités à 1
    max_astreintes = np.zeros_like(p) + max_astreintes if np.isscalar(max_astreintes) else max_astreintes
    # pas le droit à plus de n_semaines par an, tout en restant normalisé à un
    i = p > max_astreintes / n_semaines
    if np.sum(i):
        p[i] = max_astreintes[i] / n_semaines
        p[~i] = p[~i] * (1 - np.sum(p[i])) / np.sum(p[~i])
    # on répartit du mieux possible les arrondis selon les affinités
    f = n_semaines / p.sum()
    n = np.floor(f * p).astype(int)
    decimal = f * p - n
    n_missing = int(n_semaines - n.sum())
    # Indices des plus grandes décimales
    i = np.argsort(-decimal)[:n_missing]  # stable=True on np >= 2.0
    n[i] += 1
    return n


def _assignation(counts, seed=None):
    """
    Assigne les astreintes a partir d'un vecteur ou chaque entrée représente le nombre d'astreintes
    par personne.
    :param counts:
    :param seed:
    :return:
    """
    if seed is not None:
        np.random.seed(seed)
    n_semaines = counts.sum()
    assign = np.zeros(n_semaines, dtype=int)
    remaining = counts.copy()
    derniere_pioche = np.zeros_like(counts)
    for i in np.arange(n_semaines):
        j = np.lexsort((derniere_pioche, -remaining), axis=0)[0]
        assign[i] = j
        remaining[j] -= 1
        derniere_pioche[j] = i
    return assign


def _sites2effectifs(df_sites: pd.DataFrame) -> pd.DataFrame:
    """
    Crée une dataframe d'effectifs fictive à partir d'une dataframe sites
    Les techs AGA sont nommés A0 - A1 ... , les techs respi R0 - R1 ...
    :param df_sites:
    :return: df_effectifs
    """
    df_effectifs = []
    for j in range(df_sites.shape[0]):
        df_effectifs.append(
            pd.DataFrame(
                {
                    'specialite': ['aga'] * df_sites.loc[j, 'aga'] + ['respi'] * df_sites.loc[j, 'respi'],
                    'nom': [f'A{i}' for i in np.arange(df_sites.loc[j, 'aga'])]
                    + [f'R{i}' for i in np.arange(df_sites.loc[j, 'respi'])],
                    'site': df_sites.loc[j, 'nom'],
                }
            )
        )
    df_effectifs = pd.concat(df_effectifs)
    df_effectifs['preference'] = 1
    df_effectifs['id_tech'] = np.arange(df_effectifs.shape[0])
    df_effectifs.reset_index(inplace=True)
    return df_effectifs


def _shuffle_techs(itechs, semaines=None, n_iter=10_000):
    semaines = np.arange(itechs) if semaines is None else semaines

    def _varp(itechs, semaines):
        svar, nviol, ndelais = (0, 0, 0)
        for t in np.unique(itechs):
            it = np.where(itechs == t)[0]
            if len(it) <= 1:
                continue
            dt = np.diff(semaines[it])
            svar += np.var(dt)
            nviol += np.sum(dt == 1)
            ndelais += np.sum(dt == 2) / 4
        return svar, nviol, ndelais

    var_ref, viol_ref, court_ref = _varp(itechs, semaines)
    _logger.debug(f'permutations, variance initiale: {var_ref}, consecutives:  {viol_ref}')
    # on permute n_iter fois et on ne retient que les permutations qui font baisser la variance
    for _ in np.arange(n_iter):
        tt = itechs.copy()
        ii = np.random.choice(np.arange(itechs.size), 2, replace=False)
        tt[ii] = tt[np.flipud(ii)]
        var, viol, courtes = _varp(tt, semaines)
        # on rejette si on a une astreinte consécutive de plus
        if viol > viol_ref:
            continue
        # on rejette si les astreintes courtes sont plus importantes
        if courtes > court_ref:
            continue
        # la variance a baissé, on accepte la permutation
        if (var < var_ref) or (viol < viol_ref):
            itechs = tt.copy()
            var_ref, viol_ref = (var, viol)
    _logger.debug(f'permutations, variance acceptée: {var_ref}, consécutives: {viol_ref}')
    return itechs, viol_ref


def _shuffle_sites(planning, n_iter=10_000):
    """
    :param planning: (nrails, nsemaines)
    :param n_iter
    :return:
    """
    rng = np.random.default_rng()
    ordre = rng.permutation(planning.shape[1])

    def _varp(p):
        svar = 0
        for site in np.unique(p):
            for r in np.arange(p.shape[0]):
                dd = np.diff(np.where(site == p[r, :])[0])
                svar += np.var(dd)
            return svar

    svar_ref = _varp(planning[:, ordre])
    _logger.debug(f'sites permutations, variance initiale: {svar_ref}')
    # on permute n_iter fois et on ne retient que les permutations qui font baisser la variance
    for _ in np.arange(n_iter):
        ordre_ = ordre.copy()
        ii = np.random.choice(np.arange(52), 2, replace=False)
        ordre_[ii] = ordre_[np.flipud(ii)]
        svar = _varp(planning[:, ordre_])
        # la variance a baissé, on accepte la permutation
        if svar <= svar_ref:
            ordre = ordre_.copy()
            svar_ref = svar
    _logger.debug(f'sites permutations, variance acceptee: {svar_ref}')
    return ordre


def _planning_sites(counts, n_iter=0, rails=None):
    """
    Organise le planning par site pour un nombre d'astreintes par site et par spécialité
    :param counts: np.array (nrails, nsites)
    :param shuffle: bool. On cherche les permutations qui minimisent la variance de la diff:
     ce sont celles qui répartissent le mieux les astreintes au long de l'année
    :param rails:list [nrails,] avec les spécialités des rails: 'mixed', 'aga' ou 'respi'
    :return: np.array( nsemaines, nrails)
    """
    nr, ns = counts.shape
    planning = np.zeros((N_SEMAINES, nr), dtype=int) - 1
    for week in np.arange(N_SEMAINES):
        counts_ = counts.copy()
        sites_ = np.ones(nr, dtype=bool)
        for ir in np.arange(nr):
            # on cherche le site avec le plus d'astreintes a caser,
            # sauf s'il s'agit du précédent
            imaxs = np.argsort(-counts[ir, sites_])
            imax = imaxs[0]
            for im in imaxs:
                if im == planning[week - 1, ir]:
                    continue
                if counts[ir, im] > 0:
                    imax = im
                    break
            isite = np.where(sites_)[0][imax]
            planning[week, ir] = isite
            counts_[ir, :] = 0
            sites_[isite] = False
            counts[ir, isite] += -1
    if rails is None:
        code_specialite = np.arange(counts.shape[0])
    else:
        # on va optimiser les rotations en caclulant la variance, donc mixed se mets entre aga et respi
        dcodes = {'aga': 0, 'respi': 1, 'mixed': 0.5}
        code_specialite = np.array([dcodes[s] for s in rails])
    ordre = _shuffle_sites(code_specialite[planning.T], n_iter=n_iter) if n_iter else np.arange(planning.shape[0])
    return planning[ordre, :].T


def _get_rails(params, n_rotations: int):
    """
    Renvoie la liste des spécialités des rails en fonction des paramètres
    De façon à alterner les spécialités au maximum
    """
    n_mixed = n_rotations - params.min_aga - params.min_respi
    n_min = np.minimum(params.min_aga, params.min_respi)
    n_max = np.maximum(params.min_respi, params.min_aga)
    s_max = ['aga', 'respi'][np.argmax([params.min_aga, params.min_respi])]
    s_min = str(np.setdiff1d(['aga', 'respi'], s_max)[0])
    # on alterne les spécialités
    rails = [s_max] * (n_max - n_min) + [s_min, s_max] * (n_min) + ['mixed'] * n_mixed
    return rails, n_mixed


def _calcul_rotations(df_sites: pd.DataFrame, df_effectifs: pd.DataFrame, params: models.Parametres):
    n_sites = df_sites.shape[0]
    # on prend la liste des rotations, en alternant les spécialités
    rails, n_mixed = _get_rails(params, n_rotations=df_sites.rotations.sum())
    df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
    if n_sites == 1:
        df_rail.loc[:, df_sites['nom']] = N_SEMAINES
        sites_per_rail = np.zeros((len(rails), N_SEMAINES), dtype=int)
    else:
        rails = ['aga'] * params.min_aga + ['respi'] * params.min_respi + ['mixed'] * n_mixed
        df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
        site_preference = np.ones(n_sites)
        for ir, rail in df_rail.iterrows():
            if rail['specialite'] == 'mixed':
                npax = df_sites.loc[:, ['aga', 'respi']].values.sum(axis=1)
                n_rails = n_mixed
            else:
                npax = df_sites.loc[:, rail.specialite].values
                n_rails = params.min_aga if rail['specialite'] == 'aga' else params.min_respi
            df_rail.loc[ir, df_sites['nom']] = _repartition(
                site_preference, max_astreintes=npax * params.max_astreintes / n_rails
            )
            # on essaie de compenser avec les rails suivants pour balancer entre les sites
            site_preference = 1 / ((p := df_rail[df_sites['nom']].sum(axis=0).values) / sum(p))
        magic_square = df_rail[df_sites['nom']].values
        # il peut y avoir des cas où certains sites n'ont pas 52 semaines mais on peut essayer de trouver
        # une solution en reprenant davantage des spécialités pour lesquelles le site a suffisamment d'effectifs
        if not np.all(np.sum(magic_square, axis=0) == 52):
            if n_mixed > 0:
                # c'est un cas en pratique rare, il faut au moins 4 sites avec un mixed, et trop peu d'effectifs pour une solution simple
                raise NotImplementedError(
                    "Dans le cas où l'assignation initiale ne converge pas, il ne peut pas avoir de rotations mixtes"
                )
            # c'est la dernière chance de possibilité d'une solution
            _logger.debug("Il faut rebalancer les rotations car certains sites manquent d'effectifs")
            # ce sont les indices des spécialités / sites qui ne manquent pas d'effectifs et peuvent être réparties
            malleables = (
                np.r_[
                    np.tile(N_SEMAINES / df_sites['aga'].values * params.min_aga / n_sites, (params.min_aga, 1)),
                    np.tile(N_SEMAINES / df_sites['respi'].values * params.min_respi / n_sites, (params.min_respi, 1)),
                ]
                <= params.max_astreintes
            )
            magic_square = np.zeros_like(malleables, dtype=int)
            magic_square[~malleables] = params.max_astreintes
            while True:
                while True:
                    if len(c := np.where(np.sum(malleables, axis=0) == 1)[0]):
                        _logger.debug(f'\n{~malleables}, \n {magic_square}')
                        c = c[0]
                        magic_square[malleables[:, c], c] = N_SEMAINES - np.sum(magic_square[~malleables[:, c], c])
                        malleables[malleables[:, c], c] = False
                        continue
                    elif len(r := np.where(np.sum(malleables, axis=1) == 1)[0]):
                        _logger.debug(f'\n{~malleables}, \n {magic_square}')
                        r = r[0]
                        magic_square[r, malleables[r, :]] = N_SEMAINES - np.sum(magic_square[r, ~malleables[r, :]])
                        malleables[r, malleables[r, :]] = False
                        continue
                    break
                if len(r := np.where(np.sum(magic_square, axis=1) < 52)[0]):
                    c = malleables[r[0], :]
                    npax = df_sites.loc[:, rails[r[0]]].values[c]
                    n_rails = params.min_aga if rails[r[0]] == 'aga' else params.min_respi
                    magic_square[r[0], c] = _repartition(
                        np.ones(np.sum(c)),
                        n_semaines=N_SEMAINES - magic_square[r[0], ~c],
                        max_astreintes=npax * params.max_astreintes / n_rails,
                    )
                    malleables[r[0], c] = False
                else:
                    break
            assert np.all(magic_square.sum(axis=0) == N_SEMAINES)
            assert np.all(magic_square.sum(axis=1) == N_SEMAINES)
            df_rail.loc[:, df_sites['nom']] = magic_square
        sites_per_rail = _planning_sites(df_rail.loc[:, df_sites['nom']].values, n_iter=params.n_iter_shuffle, rails=rails)

    df_planning = []
    for i, rotation in enumerate(df_rail['specialite']):
        for isemaine, isite in enumerate(sites_per_rail[i]):
            df_planning.append(
                {
                    'site': df_sites.loc[isite, 'nom'],
                    'semaine': isemaine + 1,
                    'rotation': rotation,
                    'specialite': rotation,  # pour l'instant les mixed sont séparés
                }
            )
    df_planning = pd.DataFrame(df_planning).sort_values(by='semaine')

    # il faut ventiler les 'mixed' entre les spécialités selon les effectifs, on le fait en fonction de la charge des équipes site par site
    if n_mixed > 0:
        df_cspec = df_rail.groupby(['specialite']).sum()
        for site in df_sites['nom']:
            nr_aga, nr_respi, nr_mixed = (df_cspec.loc['aga', site], df_cspec.loc['respi', site], df_cspec.loc['mixed', site])
            n_aga, n_respi = df_sites.loc[df_sites['nom'] == site, ['aga', 'respi']].values.flatten()
            n_respi_mixed = np.maximum(
                0, int(np.round(((nr_aga + nr_mixed) / n_aga - nr_respi / n_respi) / (1 / n_respi + 1 / n_aga)))
            )
            imixed = np.where(np.logical_and(df_planning['site'] == site, df_planning['rotation'] == 'mixed').values)[0]
            np.random.shuffle(imixed)
            df_planning.iloc[imixed[:n_respi_mixed], df_planning.columns.get_loc('specialite')] = 'respi'
            df_planning.iloc[imixed[n_respi_mixed:], df_planning.columns.get_loc('specialite')] = 'aga'

    for site in df_sites['nom']:
        for specialite in df_planning['specialite'].unique():  # normalement ['aga', 'respi']
            ip = np.logical_and(df_planning['site'] == site, df_planning['specialite'] == specialite)
            semaines = df_planning.loc[ip, 'semaine'].values
            df_techs_ = df_effectifs[
                np.logical_and(
                    df_effectifs['site'] == site,
                    df_effectifs['specialite'] == specialite,
                )
            ]
            n_astreintes_per_tech = _repartition(
                p=df_techs_['preference'].values,
                n_semaines=semaines.size,
                max_astreintes=params.max_astreintes,
            )
            itechs_, n_consecutives = _shuffle_techs(
                _assignation(n_astreintes_per_tech), semaines=semaines, n_iter=params.n_iter_shuffle
            )
            for col in ['nom', 'id_tech', 'preference']:
                df_planning.loc[ip, col] = df_techs_.iloc[itechs_][col].values
            assert n_consecutives == 0
    assert np.isnan(df_planning['id_tech']).sum() == 0
    # ici la dataframe résultante a les colonnes semaine | site | rotation | id_tech | specialite
    return df_planning


def rapport_planning(df_planning: pd.DataFrame):
    """
    Aggrégations du planning d'un regroupement de sites:
    par technicien
    par site
    par spécialité
    :param df_planning:
    :return:
    """
    rapports = {}
    rapports['effectifs'] = (
        df_planning.groupby(['site', 'specialite', 'id_tech'])
        .agg(
            n_astreintes=pd.NamedAgg(column='semaine', aggfunc='count'),
            nom=pd.NamedAgg(column='nom', aggfunc='first'),
            delai_min=pd.NamedAgg(column='semaine', aggfunc=lambda x: np.min(np.diff(x)) if x.size > 1 else N_SEMAINES),
        )
        .reset_index()
    )
    rapports['sites'] = (
        df_planning.groupby(['site', 'specialite']).agg(n_semaines=pd.NamedAgg(column='semaine', aggfunc='count')).reset_index()
    )
    rapports['specialite'] = (
        df_planning.groupby(['semaine', 'specialite'])
        .agg(n_astreintes=pd.NamedAgg(column='semaine', aggfunc='count'))
        .groupby('specialite')
        .min()
    )
    rapports['zone'] = df_planning.pivot_table(index='semaine', columns='site', values='rotation', aggfunc='first')
    return rapports


def validation_planning(df_planning, params: models.Parametres, rapports: dict = None):
    """
    :param df_planning:
    :param params:
    :return:
    """
    rapports = rapports if rapports is not None else rapport_planning(df_planning)
    validation = {
        'astreintes_consecutives': np.all(rapports['effectifs'].delai_min > 1),
        'quota employe depasse': np.all(rapports['effectifs'].n_astreintes <= params.max_astreintes),
        'quota sites rempli': np.all(df_planning.groupby('site').nunique()['semaine'] == N_SEMAINES),
        'quota specialites rempli': np.logical_and(
            (rapports['specialite'].loc['aga', 'n_astreintes'] if 'aga' in rapports['specialite'].index else 0) >= params.min_aga,
            (rapports['specialite'].loc['respi', 'n_astreintes'] if 'respi' in rapports['specialite'].index else 0)
            >= params.min_respi,
        ),
    }
    return validation


def separation_calendriers(df_sites, df_effectifs=None, params=None):
    """
    Pour les regroupements de site complexes, il est plus facile de séparer le problème
    :param df_sites:
    :param df_effectifs
    :return:
    """
    assert params is not None
    df_effectifs = _sites2effectifs(df_sites) if df_effectifs is None else df_effectifs
    # le but est d'arriver à une seule rotation par site et/ou un seul site
    if np.all(df_sites['rotations'] == 1) or df_sites.shape[0] == 1:
        return [{'sites': df_sites, 'effectifs': df_effectifs, 'params': params}]
    # le premier passage est pour assigner les spécialités aux regroupements, en fonction du nombre minimum de chaque
    # specialite requis
    rotations = df_sites['rotations'].values.copy()
    rails = {'aga': params.min_aga, 'respi': params.min_respi}
    all_sites, all_groups = ([], [])
    for ig in np.arange(np.max(rotations)):
        ir = rotations > 0
        rotations[ir] = rotations[ir] - 1
        ns = np.sum(ir)
        # ici on donne 50/50 si il n'y a pas de préférence pour la spécialité
        ispe = np.mod(
            np.arange(ns) + (params.min_respi > params.min_aga) + (params.min_respi == params.min_aga) * np.random.choice([1, 0]),
            2,
        )
        min_aga, min_respi = (np.sum(ispe == 0), np.sum(ispe == 1))
        rails['aga'] -= min_aga
        rails['respi'] -= min_respi
        all_groups.append({'min_aga': min_aga, 'min_respi': min_respi, 'n_sites': ns})
        all_sites.append(pd.DataFrame({'nom': df_sites['nom'][ir], 'respi': -1, 'aga': -1, 'rotations': 1, 'groupe': ig}))
    all_sites = pd.concat(all_sites)
    all_groups = pd.DataFrame(all_groups)
    # le deuxieme passage permet de répartir les effectifs en fonction des spécialités ci-dessus
    df_effectifs['groupe'] = -1
    for _, site in df_sites.iterrows():
        isites = all_sites['nom'] == site.nom
        ig = all_sites.loc[isites, 'groupe'].unique()
        ratios = all_groups.loc[ig, ['min_aga', 'min_respi']].values / all_groups.loc[ig, 'n_sites'].values[:, np.newaxis]
        for ispe, specialite in enumerate(['aga', 'respi']):
            rep = _repartition(ratios[:, ispe], n_semaines=site[specialite], max_astreintes=999)
            all_sites.loc[isites, specialite] = rep
            ie = np.where((df_effectifs['site'] == site.nom) & (df_effectifs['specialite'] == specialite))[0]
            np.random.shuffle(ie)
            for igg, iee in zip(ig, np.split(ie, np.cumsum(rep[:-1]))):
                df_effectifs.loc[iee, 'groupe'] = igg
    # au final, on crée les dataframes sites, dataframe effectif et params pour chaque groupe dans une liste de dictionaires
    dse = []
    for ig, df_sites_ in all_sites.groupby('groupe'):
        params_ = params.model_dump() | {f: all_groups.loc[ig, f] for f in ['min_aga', 'min_respi']}
        dse.append(
            {
                'sites': df_sites_.copy().drop(columns='groupe').reset_index(drop=True),
                'effectifs': df_effectifs[df_effectifs['groupe'] == ig].copy().drop(columns='groupe').reset_index(drop=True),
                'params': models.Parametres(**params_),
            }
        )
    return dse


def genere_planning(
    df_sites: pd.DataFrame,
    params: models.Parametres = None,
    df_effectifs: pd.DataFrame = None,
    mode='raise',
):
    params = models.Parametres() if params is None else params
    models.Parametres.model_validate(params)
    # specialite  id_tech nom   site
    df_effectifs = _sites2effectifs(df_sites) if df_effectifs is None else df_effectifs

    liste_sites_effectifs = separation_calendriers(df_sites, df_effectifs, params=params)
    df_planning = []
    for dse in liste_sites_effectifs:
        # semaine   site  rotation  id_tech specialite
        df_planning.append(_calcul_rotations(dse['sites'], dse['effectifs'], params=dse['params']))
    df_planning = pd.concat(df_planning).sort_values(['site', 'specialite', 'semaine'])
    # validation du planning
    rapports = rapport_planning(df_planning)
    validation = validation_planning(df_planning, params=params, rapports=rapports)
    for k, v in validation.items():
        if not v:
            _logger.warning(f'{k} failed for site {df_sites}')
        if mode == 'raise':
            assert v, f'{k}'
    return df_planning, rapports, validation
