# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:04:41 2019

@author: michaelek
"""
import io
import numpy as np
from gistools import vector
from allotools import AlloUsage
# from hydrolm import LM
import os
import sys
import pandas as pd
import geopandas as gpd
import nzrec
import booklet

# try:
#     import plotly.offline as py
#     import plotly.graph_objs as go
# except:
#     print('install plotly for plot functions to work')

#####################################
### Parameters

# base_dir = os.path.dirname(os.path.abspath( __file__ ))
# base_dir = os.path.realpath(os.path.dirname(__file__))

# print(base_dir)

# with open(os.path.join(base_dir, 'parameters.yml')) as param2:
#     param = yaml.safe_load(param2)

# # datasets_path = os.path.join(base_dir, 'datasets')
# outputs = param['output']

# catch_key_base = 'tethys/station_misc/{station_id}.catchment.geojson.zst'

####################################
### Testing

# base_dir = os.path.split(os.path.realpath(os.path.dirname(__file__)))[0]

# with open(os.path.join(base_dir, 'parameters.yml')) as param2:
#     param1 = yaml.safe_load(param2)

# flow_remote = param1['remote']['flow']
# usage_remote = param1['remote']['usage']
#

# flow_stations_path = '/home/mike/git/HRC-flow-nat/data/flow_sites.gpkg'
# flow_data_path = '/home/mike/git/HRC-flow-nat/data/flow_data_daily.blt'
# permits_path = '/home/mike/git/HRC-flow-nat/data/permits.blt'
# usage_path = '/home/mike/git/HRC-flow-nat/data/abstraction_data_daily.blt'
# nzrec_path = '/home/mike/git/nzrec/data'


# from_date='2010-07-01'
# to_date='2020-06-30'
# product_code='quality_controlled_data'
# min_gaugings=10
# output_path=os.path.join(base_dir, 'tests')
# local_tz='Etc/GMT-12'
# station_id=['0bc0762fac7423261610b50f', '0ba603f66f55a19d18cbeb81', '0c6b76f9ff6fcf2e103f5e84', '2ec4a2cfa71dd4811eec25e4', '0d1024b9975b573e515ebd62']
# station_id=['0d1024b9975b573e515ebd62']
# ref=None
#
#
# self = FlowNat(flow_remote, usage_remote, from_date, to_date, product_code, min_gaugings, station_id, ref, output_path)
#
# stns_all = self.stations_all.station_id.unique().tolist().copy()
#
# stns1 = self.process_stations(stns_all)
#
# nat_flow = self.naturalisation()


# wap1 = 'SW/0082'
#
# a1 = AlloUsage(from_date='2015-06-30', to_date='2016-06-30', wap_filter={'wap': [wap1]})
#
# res1 = a1.get_ts(['allo', 'usage'], 'D', ['wap'])

#######################################
### Class


class FlowNat(object):
    """
    Class to perform several operations to ultimately naturalise flow data.
    Initialise the class with the following parameters.

    Parameters
    ----------
    from_date : str
        The start date for the flow record.
    to_date : str
        The end of of the flow record.
    min_gaugings : int
        The minimum number of gaugings required for the regressions. Default is 8.
    rec_data_code : str
        Either 'RAW' for the raw telemetered recorder data, or 'Primary' for the quality controlled recorder data. Default is 'Primary'.
    input_sites : str, int, list, or None
        Flow sites (either recorder or gauging) to be naturalised. If None, then the input_sites need to be defined later. Default is None.
    output_path : str or None
        Path to save the processed data, or None to not save them.
    load_rec : bool
        should the REC rivers and catchment GIS layers be loaded in at initiation?

    Returns
    -------
    FlowNat instance
    """
    def __init__(self, flow_stations_path, flow_data_path, permits_path, usage_path, nzrec_path, from_date=None, to_date=None, use_type_mapping={}, default_sd_ratio=0.35, output_path=None):
        """
        Class to perform several operations to ultimately naturalise flow data.
        Initialise the class with the following parameters.

        Parameters
        ----------
        from_date : str
            The start date for the flow record.
        to_date : str
            The end of of the flow record.
        min_gaugings : int
            The minimum number of gaugings required for the regressions. Default is 8.
        rec_data_code : str
            Either 'RAW' for the raw telemetered recorder data, or 'Primary' for the quality controlled recorder data. Default is 'Primary'.
        input_sites : str, int, list, or None
            Flow sites (either recorder or gauging) to be naturalised. If None, then the input_sites need to be defined later. Default is None.
        output_path : str or None
            Path to save the processed data, or None to not save them.
        catch_del : str
            Defines what should be used for the catchments associated with flow sites. 'rec' will perform a catchment delineation on-the-fly using the REC rivers and catchments GIS layers, 'internal' will use the pre-generated catchments stored in the package, or a path to a shapefile will use a user created catchments layer. The shapefile must at least have a column named ExtSiteID with the flow site numbers associated with the catchment geometry.

        Returns
        -------
        FlowNat instance
        """
        setattr(self, 'from_date', from_date)
        setattr(self, 'to_date', to_date)
        # setattr(self, 'min_gaugings', min_gaugings)
        # setattr(self, 'flow_remote', flow_remote)
        # setattr(self, 'usage_remote', usage_remote)
        # setattr(self, 'product_code', product_code)
        # setattr(self, 'local_tz', local_tz)

        self.flow_stations_path = flow_stations_path
        self.flow_data_path = flow_data_path
        self.permits_path = permits_path
        self.usage_path = usage_path
        self.nzrec_path = nzrec_path
        self.default_sd_ratio = default_sd_ratio
        self.use_type_mapping = use_type_mapping

        self.save_path(output_path)

        _ = self.get_all_flow_stations()

        allo0 = AlloUsage(permits_path, usage_path, from_date, to_date, use_type_mapping=use_type_mapping, default_sd_ratio=default_sd_ratio)

        self.waps_all = vector.xy_to_gpd(['permit_id', 'wap', 'sd_ratio'], 'lon', 'lat', allo0.waps, 4326)
        self.permits_all = allo0.permits

        # if (isinstance(station_id, list)) or (isinstance(ref, list)):
        #     _ = self.process_stations(station_id=station_id, ref=ref)


    def save_path(self, output_path=None):
        """
    
        """
        if output_path is None:
            pass
        elif isinstance(output_path, str):
            if not os.path.exists(output_path):
                os.makedirs(output_path)
    
            setattr(self, 'output_path', output_path)


    def get_all_flow_stations(self):
        """
        Function to process the flow datasets

        Parameters
        ----------
        from_date : str
            The start date for the flow record.
        to_date : str
            The end of of the flow record.
        min_gaugings : int
            The minimum number of gaugings required for the regressions. Default is 8.
        rec_data_code : str
            Either 'RAW' for the raw telemetered recorder data, or 'Primary' for the quality controlled recorder data. Default is 'Primary'.

        Returns
        -------
        DataFrame
        """
        # tethys1 = Tethys([self.flow_remote])

        # flow_ds = [ds for ds in tethys1.datasets if (ds['parameter'] == 'streamflow') and (ds['product_code'] == self.product_code) and (ds['frequency_interval'] == '24H') and (ds['utc_offset'] == '12H') and (ds['method'] == 'sensor_recording')]
        # flow_ds.extend([ds for ds in tethys1.datasets if (ds['parameter'] == 'streamflow') and (ds['product_code'] == self.product_code) and (ds['frequency_interval'] == 'None') and (ds['method'] == 'field_activity')])

        # stns_list = []

        # for ds in flow_ds:
        #     stns1 = tethys1.get_stations(ds['dataset_id'])
        #     stns_list.extend(stns1)

        # stns_list2 = [s for s in stns_list if s['dimensions']['time'] >= self.min_gaugings]

        # stns_list3 = [{'dataset_id': s['dataset_id'], 'station_id': s['station_id'], 'ref': s['ref'], 'geometry': Point(s['geometry']['coordinates']), 'count': s['dimensions']['time'], 'from_date': s['time_range']['from_date'], 'to_date': s['time_range']['to_date']} for s in stns_list2]
        # [s.update({'from_date': s['from_date'] + '+00:00', 'to_date': s['to_date'] + '+00:00'}) for s in stns_list3 if not '+00:00' in s['from_date']]

        # stns_summ = gpd.GeoDataFrame(pd.DataFrame(stns_list3), geometry='geometry', crs=4326)
        # try:
        #     stns_summ['from_date'] = pd.to_datetime(stns_summ['from_date']).dt.tz_convert(self.local_tz).dt.tz_localize(None)
        #     stns_summ['to_date'] = pd.to_datetime(stns_summ['to_date']).dt.tz_convert(self.local_tz).dt.tz_localize(None)
        # except:
        #     pass

        # if isinstance(self.from_date, str):
        #     from_date1 = pd.Timestamp(self.from_date)
        #     stns_summ = stns_summ[stns_summ['from_date'] <= from_date1]
        # if isinstance(self.to_date, str):
        #     to_date1 = pd.Timestamp(self.to_date)
        #     stns_summ = stns_summ[stns_summ['to_date'] >= to_date1]

        # setattr(self, 'stations_all', stns_summ)
        # setattr(self, '_tethys_flow', tethys1)
        # setattr(self, 'flow_datasets_all', flow_ds)

        self.stations_all = gpd.read_file(self.flow_stations_path)

        return self.stations_all


    def process_stations(self, station_ids=None, refs=None):
        """
        Function to process the sites.

        Parameters
        ----------
        input_sites : str, int, list, or None
            Flow sites (either recorder or gauging) to be naturalised. If None, then the input_sites need to be defined later. Default is None.

        Returns
        -------
        DataFrame
        """
        ## Checks
        # if (not isinstance(station_ids, list)) and (not isinstance(refs, list)):
        #     raise ValueError('station_ids and refs must be lists')

        ## Filter
        stns1 = self.stations_all.copy()

        bad_stns = []

        if isinstance(station_ids, list):
            stns1 = stns1[stns1['station_id'].isin(station_ids)]
            [bad_stns.extend([s['ref']]) for i, s in stns1.iterrows() if s['station_id'] not in station_ids]
        if isinstance(refs, list):
            stns1 = stns1[stns1['ref'].isin(refs)]
            [bad_stns.extend([s['ref']]) for i, s in stns1.iterrows() if s['ref'] not in refs]

        if bad_stns:
            print(', '.join(bad_stns) + ' stations are not available for naturalisation')

        ## Save if required
        # if hasattr(self, 'output_path'):
        #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')
        #     flow_sites_shp = outputs['flow_sites_shp'].format(run_date=run_time)
        #     save1 = stns1.copy()
        #     save1['from_date'] = save1['from_date'].astype(str)
        #     save1['to_date'] = save1['to_date'].astype(str)
        #     save1.to_file(os.path.join(self.output_path, flow_sites_shp))

        ## Drop duplicate stations
        stns2 = stns1.drop_duplicates('station_id').rename(columns={'SiteName': 'ref'})

        setattr(self, 'stations', stns2)

        ## Filter flow datasets
        # stn_ds = stns2['dataset_id'].unique()
        # flow_ds1 = self.flow_datasets_all.copy()
        # flow_ds2 = [ds for ds in flow_ds1 if ds['dataset_id'] in stn_ds]

        # setattr(self, 'flow_datasets', flow_ds2)

        ## Remove existing attributes if they exist
        if hasattr(self, 'catch'):
            delattr(self, 'catch')
        if hasattr(self, 'waps'):
            delattr(self, 'waps')
        if hasattr(self, 'flow'):
            delattr(self, 'flow')
        if hasattr(self, 'usage_rate'):
            delattr(self, 'usage_rate')
        if hasattr(self, 'nat_flow'):
            delattr(self, 'nat_flow')

        return stns1


    # @staticmethod
    # def _get_catchment(inputs):
    #     """

    #     """
    #     station_id = inputs['station_id']
    #     bucket = inputs['bucket']
    #     public_url = inputs['public_url']

    #     key1 = catch_key_base.format(station_id=station_id)
    #     try:
    #         obj0 = utils.get_object_s3(key1, public_url=public_url, bucket=bucket, counter=1)
    #         dctx = zstd.ZstdDecompressor()
    #         obj1 = dctx.decompress(obj0)
    #         b2 = io.BytesIO(obj1)
    #         c1 = gpd.read_file(b2)
    #     except:
    #         c1 = gpd.GeoDataFrame(columns=['id', 'area', 'dataset_id', 'distance', 'nzsegment', 'ref', 'station_id', 'geometry'])

    #     return c1


    def get_catchments(self):
        """

        """
        if not hasattr(self, 'stations'):
            raise ValueError('Please run the process_stations method.')

        stns = self.stations.copy()

        w0 = nzrec.Water(self.nzrec_path)

        catch_list = []
        for i, row in stns.iterrows():
            geo = row.geometry
            stn_id = row.station_id
            coords = np.asarray(geo.coords[0])
            way0 = w0.nearest_way_within_catchments(coords, 0.1)
            up0 = way0.upstream()
            catch0 = up0.catchments().to_gpd()
            catch0['station_id'] = stn_id
            catch_list.append(catch0)

        catch1 = pd.concat(catch_list).reset_index(drop=True)

        setattr(self, 'catch', catch1)
        return catch1




        # stns = self.stations.copy()
        # stn_ids = stns.station_id.unique()

        # public_url = self.flow_remote['public_url']
        # bucket = self.flow_remote['bucket']

        # input_list = [{'public_url': public_url, 'bucket': bucket, 'station_id': s} for s in stn_ids]

        # output = ThreadPool(threads).map(self._get_catchment, input_list)

        # catch1 = pd.concat(output).drop('id', axis=1)
        # catch1.crs = pyproj.CRS(2193)
        # catch1 = catch1.to_crs(4326)

        # ## Save if required
        # if hasattr(self, 'output_path'):
        #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')
        #     catch_del_shp = outputs['catch_del_shp'].format(run_date=run_time)
        #     catch1.to_file(os.path.join(self.output_path, catch_del_shp))

        # setattr(self, 'catch', catch1)
        # return catch1


    # def get_waps(self):
    #     """

    #     """
    #     tethys1 = Tethys([self.usage_remote])

    #     usage_ds = [ds for ds in tethys1.datasets if (ds['parameter'] == 'water_use') and (ds['product_code'] == 'raw_data') and (ds['frequency_interval'] == '24H') and (ds['utc_offset'] == '12H') and (ds['method'] == 'sensor_recording')]

    #     stns_list = []

    #     for ds in usage_ds:
    #         stns1 = tethys1.get_stations(ds['dataset_id'])
    #         stns_list.extend(stns1)

    #     stns_list3 = [{'dataset_id': s['dataset_id'], 'station_id': s['station_id'], 'ref': s['ref'], 'geometry': Point(s['geometry']['coordinates']), 'from_date': s['time_range']['from_date'], 'to_date': s['time_range']['to_date']} for s in stns_list]
    #     [s.update({'from_date': s['from_date'] + '+00:00', 'to_date': s['to_date'] + '+00:00'}) for s in stns_list3 if not '+00:00' in s['from_date']]

    #     stns_summ = gpd.GeoDataFrame(pd.DataFrame(stns_list3), geometry='geometry', crs=4326)

    #     try:
    #         stns_summ['from_date'] = pd.to_datetime(stns_summ['from_date']).dt.tz_convert(self.local_tz).dt.tz_localize(None)
    #         stns_summ['to_date'] = pd.to_datetime(stns_summ['to_date']).dt.tz_convert(self.local_tz).dt.tz_localize(None)
    #     except:
    #         pass

    #     if isinstance(self.from_date, str):
    #         from_date1 = pd.Timestamp(self.from_date)
    #         stns_summ = stns_summ[stns_summ['to_date'] >= from_date1]
    #     if isinstance(self.to_date, str):
    #         to_date1 = pd.Timestamp(self.to_date)
    #         stns_summ = stns_summ[stns_summ['from_date'] <= to_date1]

    #     setattr(self, 'waps_all', stns_summ)
    #     setattr(self, '_tethys_usage', tethys1)
    #     setattr(self, 'usage_datasets', usage_ds)

    #     return stns_summ


    def get_upstream_waps(self):
        """
        Function to determine the upstream water abstraction sites from the catchment delineation.

        Returns
        -------
        DataFrame
            allocation data
        """
        waps_all = self.waps_all.drop('permit_id', axis=1).drop_duplicates(subset='wap').to_crs(4326).copy()

        if not hasattr(self, 'catch'):
            catch1 = self.get_catchments()
        else:
            catch1 = self.catch.copy()

        # waps.rename(columns={'station_id': 'wap_stn_id', 'dataset_id': 'wap_ds_id', 'ref': 'wap'}, inplace=True)

        ### WAP selection
        waps_catch, poly1 = vector.pts_poly_join(waps_all, catch1, 'station_id')

        ### Get crc data
        if waps_catch.empty:
            raise ValueError('No WAPs were found in the polygon(s)')
        # else:
        #     waps_sel = waps_all[waps_all.wap.isin(waps_catch.wap.unique())].copy()

            ## Save if required
            # if hasattr(self, 'output_path'):
            #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')

            #     save1 = waps_sel.copy()
            #     save1['from_date'] = save1['from_date'].astype(str)
            #     save1['to_date'] = save1['to_date'].astype(str)

            #     waps_shp = outputs['waps_shp'].format(run_date=run_time)
            #     save1.to_file(os.path.join(self.output_path, waps_shp))

        ## Return
        setattr(self, 'waps_catch', waps_catch)

        return waps_catch


    def get_usage(self):
        """

        """
        if not hasattr(self, 'waps_catch'):
            waps_catch = self.get_upstream_waps()
        else:
            waps_catch = self.waps_catch.copy()

        # waps2 = waps_catch.groupby(['wap_ds_id', 'wap_stn_id']).first().reset_index()

        wap_ids = waps_catch.wap.unique().tolist()

        allo1 = AlloUsage(self.permits_path, self.usage_path, wap_filter={'wap': wap_ids}, from_date=self.from_date, to_date=self.to_date, use_type_mapping=self.use_type_mapping, default_sd_ratio=self.default_sd_ratio)

        usage1 = allo1.get_ts(['allo', 'sd_rates'], 'D', ['wap'])
        usage1a = usage1[(usage1['total_allo'] > 0) & (usage1['sw_allo'] > 0)].dropna().copy()
        if 'sd_rate' not in usage1a.columns:
            usage1a['sd_rate'] = 0
        usage2 = usage1a[['sw_allo', 'sd_rate']].reset_index()

        usage3 = pd.merge(waps_catch[['wap', 'station_id']], usage2, on='wap')

        ## Aggregate by flow station id and date
        usage4 = usage3.groupby(['station_id', 'date'])[['sw_allo', 'sd_rate']].sum()
        usage5 = (usage4 / 24 / 60 / 60).round(3)

        usage5.rename(columns={'sw_allo': 'allocation', 'sd_rate': 'stream depletion'}, inplace=True)

        ## Aggregate by flow station id, wap station id, and date
        usage6 = usage3.groupby(['station_id', 'wap', 'date'])[['sw_allo', 'sd_rate']].sum()
        usage7 = (usage6 / 24 / 60 / 60).round(3)

        usage7.rename(columns={'sw_allo': 'allocation', 'sd_rate': 'stream depletion'}, inplace=True)

        ## Save results
        # if hasattr(self, 'output_path'):
        #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')

        #     usage_rate_wap_csv = outputs['usage_rate_wap_csv'].format(run_date=run_time)
        #     usage1.to_csv(os.path.join(self.output_path, usage_rate_wap_csv))

        setattr(self, 'usage_rate', usage5.reset_index())
        setattr(self, 'usage_rate_wap', usage7.reset_index())

        return usage5.reset_index()


    def get_flow(self, buffer_dis=60000):
        """
        Function to query and/or estimate flow at the input_sites.

        Parameters
        ----------
        buffer_dis : int
            The search radius for the regressions in meters.

        Returns
        -------
        DataFrame of Flow
        """
        flow_list = []
        with booklet.open(self.flow_data_path) as f:
            # print(list(f.keys()))
            for stn_id, data in f.items():
                data0 = data.set_index('time').loc[slice(self.from_date, self.to_date)]
                if not data0.empty:
                    flow_list.append(data0)

        flow = pd.concat(flow_list, axis=1)

        setattr(self, 'flow', flow)
        # setattr(self, 'reg_flow', reg_df)
        return flow




        # ### Prep the stations and other inputs
        # flow_ds = self.flow_datasets.copy()
        # tethys1 = self._tethys_flow
        # stns = self.stations.copy()
        # rec_ds_id = [ds for ds in self.flow_datasets_all if ds['method'] == 'sensor_recording'][0]['dataset_id']
        # man_ds_id = [ds for ds in self.flow_datasets_all if ds['method'] == 'field_activity'][0]['dataset_id']

        # methods = [m['method'] for m in flow_ds]

        # rec_stns = self.stations_all[self.stations_all.dataset_id == rec_ds_id].to_crs(2193).copy()

        # if self.from_date is None:
        #     from_date1 = None
        # else:
        #     from_date1 = pd.Timestamp(self.from_date, tz=self.local_tz).tz_convert('utc').tz_localize(None)
        # if self.to_date is None:
        #     to_date1 = None
        # else:
        #     to_date1 = pd.Timestamp(self.to_date, tz=self.local_tz).tz_convert('utc').tz_localize(None)

        # ### Iterate through the two datasets
        # for ds in flow_ds:
        #     ds_id = ds['dataset_id']
        #     stns1 = stns[stns['dataset_id'] == ds_id].copy()
        #     stn_ids = stns1['station_id'].unique().tolist()

        #     flow_data1 = tethys1.get_results(ds_id, stn_ids, from_date=from_date1, to_date=to_date1, squeeze_dims=True, threads=threads)

        #     val2 = flow_data1[['streamflow', 'station_id']].drop('height').to_dataframe().reset_index()
        #     flow_data = val2.drop('geometry', axis=1).dropna()

        #     flow_data['time'] = flow_data['time'].dt.tz_localize('utc').dt.tz_convert(self.local_tz).dt.tz_localize(None).dt.floor('D')

        #     flow_data = flow_data.groupby(['station_id', 'time']).mean().reset_index()

        #     if ds['method'] == 'field_activity':

        #         man_ts_data2 = flow_data.set_index(['station_id', 'time'])['streamflow'].unstack(0)

        #         ## Determine which sites are within the buffer of the manual sites
        #         man_stns = stns[stns['dataset_id'] == man_ds_id].to_crs(2193).copy()
        #         man_stns.set_index('station_id', inplace=True)
        #         man_stns['geometry'] = man_stns.buffer(buffer_dis)

        #         buff_sites_dict = {}

        #         for index in man_stns.index:
        #             buff_sites1 = vector.sel_sites_poly(rec_stns, man_stns.loc[[index]])
        #             buff_sites_dict[index] = buff_sites1['station_id'].tolist()

        #         buff_sites_list = [item for sublist in buff_sites_dict.values() for item in sublist]
        #         buff_sites = list(set(buff_sites_list))

        #         ## Pull out recorder data needed for all manual sites
        #         rec_data1 = tethys1.get_results(rec_ds_id, buff_sites, from_date=from_date1, to_date=to_date1, squeeze_dims=True, threads=threads)

        #         val2 = rec_data1[['streamflow', 'station_id']].drop('height').to_dataframe().reset_index()
        #         rec_data = val2.drop('geometry', axis=1).dropna()

        #         rec_data['time'] = rec_data['time'].dt.tz_localize('utc').dt.tz_convert(self.local_tz).dt.tz_localize(None).dt.floor('D')
        #         rec_data1 = rec_data.groupby(['station_id', 'time']).mean()
        #         rec_data1 = rec_data1['streamflow'].unstack(0).interpolate('time', limit=10)

        #         ## Run through regressions
        #         reg_lst = []
        #         new_lst = []

        #         for key, lst in buff_sites_dict.items():
        #             # print(key)
        #             man_rec_ts_data3 = rec_data1.loc[:, rec_data1.columns.isin(lst)].copy()
        #             man_rec_ts_data3[man_rec_ts_data3 <= 0] = np.nan

        #             man_ts_data3 = man_ts_data2.loc[:, [key]].copy()
        #             man_ts_data3[man_ts_data3 <= 0] = np.nan

        #             lm1 = LM(man_rec_ts_data3, man_ts_data3)
        #             res1 = lm1.predict(n_ind=1, x_transform='log', y_transform='log', min_obs=self.min_gaugings)
        #             if res1 is None:
        #                 continue

        #             res1_f = res1.summary_df['f value'].iloc[0]
        #             res2 = lm1.predict(n_ind=2, x_transform='log', y_transform='log', min_obs=self.min_gaugings)
        #             if res2 is not None:
        #                 res2_f = res2.summary_df['f value'].iloc[0]
        #             else:
        #                 res2_f = 0

        #             f = [res1_f, res2_f]

        #             val = f.index(max(f))

        #             if val == 0:
        #                 reg_lst.append(res1.summary_df)

        #                 s1 = res1.summary_df.iloc[0]

        #                 d1 = man_rec_ts_data3[s1['x sites']].copy()
        #                 d1[d1 <= 0] = 0.001

        #                 new_data1 = np.exp(np.log(d1) * float(s1['x slopes']) + float(s1['y intercept']))
        #                 new_data1.name = key
        #                 new_data1[new_data1 <= 0] = 0
        #             else:
        #                 reg_lst.append(res2.summary_df)

        #                 s1 = res2.summary_df.iloc[0]
        #                 x_sites = s1['x sites'].split(', ')
        #                 x_slopes = [float(s) for s in s1['x slopes'].split(', ')]
        #                 intercept = float(s1['y intercept'])

        #                 d1 = man_rec_ts_data3[x_sites[0]].copy()
        #                 d1[d1 <= 0] = 0.001
        #                 d2 = man_rec_ts_data3[x_sites[1]].copy()
        #                 d2[d2 <= 0] = 0.001

        #                 new_data1 = np.exp((np.log(d1) * float(x_slopes[0])) + (np.log(d2) * float(x_slopes[1])) + intercept)
        #                 new_data1.name = key
        #                 new_data1[new_data1 <= 0] = 0

        #             new_lst.append(new_data1)

        #         new_data2 = pd.concat(new_lst, axis=1)
        #         reg_df = pd.concat(reg_lst).reset_index()

        #     elif ds['method'] == 'sensor_recording':
        #         rec_flow_data = flow_data.set_index(['station_id', 'time'])['streamflow'].unstack(0)
        #     else:
        #         raise ValueError('The dataset method should be either field_activity or sensor_recording.')

        # if not 'sensor_recording' in methods:
        #     flow = new_data2.round(3)
        # elif not 'field_activity' in methods:
        #     flow = rec_flow_data.round(3)
        #     reg_df = pd.DataFrame()
        # else:
        #     flow = pd.concat([rec_flow_data, new_data2], axis=1).round(3)

        # ## Save if required
        # if hasattr(self, 'output_path'):
        #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')

        #     # stns

        #     if not reg_df.empty:
        #         reg_flow_csv = outputs['reg_flow_csv'].format(run_date=run_time)
        #         reg_df.to_csv(os.path.join(self.output_path, reg_flow_csv), index=False)

        #     flow_csv = outputs['flow_csv'].format(run_date=run_time)
        #     flow.to_csv(os.path.join(self.output_path, flow_csv))

        # setattr(self, 'flow', flow)
        # setattr(self, 'reg_flow', reg_df)
        # return flow


    def naturalisation(self):
        """
        Function to put all of the previous functions together to estimate the naturalised flow at the input_sites. It takes the estimated usage rates above each input site and adds that back to the flow.

        Returns
        -------
        DataFrame
            of measured flow, upstream usage rate, and naturalised flow
        """
        if not hasattr(self, 'usage_rate'):
            usage_daily_rate = self.get_usage()
        else:
            usage_daily_rate = self.usage_rate.copy()

        if not hasattr(self, 'flow'):
            flow = self.get_flow()
        else:
            flow = self.flow.copy()

        if usage_daily_rate.empty:
            flow2 = flow.stack().reset_index()
            flow2.columns = ['date', 'station_id', 'flow']
            flow2 = flow2.set_index(['station_id', 'date']).sort_index()
            flow2['sw_usage'] = 0
        else:

            ## Add usage to flow
            flow1 = flow.stack().reset_index()
            flow1.columns = ['date', 'station_id', 'flow']

            flow2 = pd.merge(flow1, usage_daily_rate, on=['station_id', 'date'], how='left').set_index(['station_id', 'date']).sort_index()
            flow2.loc[flow2['stream depletion'].isnull(), 'stream depletion'] = 0
            # flow2.loc[flow2['estimated usage'].isnull(), 'estimated usage'] = 0
            flow2.loc[flow2['allocation'].isnull(), 'allocation'] = 0

        flow2['nat flow'] = flow2['flow'] + flow2['stream depletion']

        ## Use the reference identifier instead of station_ids
        flow3 = pd.merge(flow2.reset_index(), self.stations[['station_id', 'ref']], on='station_id').drop('station_id', axis=1)
        flow4 = flow3.groupby(['ref', 'date']).mean().sort_index()

        # nat_flow = flow4.unstack(0).round(3)

        ## Save results
        # if hasattr(self, 'output_path'):
        #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')

        #     nat_flow_csv = outputs['nat_flow_csv'].format(run_date=run_time)
        #     nat_flow.to_csv(os.path.join(self.output_path, nat_flow_csv))

        #     setattr(self, 'nat_flow_csv', nat_flow_csv)

        setattr(self, 'nat_flow', flow4)
        return flow4


    # def plot(self, input_site):
    #     """
    #     Function to run and plot the detide results.

    #     Parameters
    #     ----------
    #     output_path : str
    #         Path to save the html file.

    #     Returns
    #     -------
    #     DataFrame or Series
    #     """

    #     if hasattr(self, 'nat_flow'):
    #         nat_flow = self.nat_flow.copy()
    #     else:
    #         nat_flow = self.naturalisation()

    #     nat_flow1 = nat_flow.loc[:, (slice(None), input_site)]
    #     nat_flow1.columns = nat_flow1.columns.droplevel(1)

    #     colors1 = ['rgb(102,194,165)', 'rgb(252,141,98)', 'rgb(252,141,0)', 'rgb(141,160,203)']

    #     orig = go.Scattergl(
    #         x=nat_flow1.index,
    #         y=nat_flow1['flow'],
    #         name = 'Recorded Flow',
    #         line = dict(color = colors1[3]),
    #         opacity = 0.8)

    #     meas_usage = go.Scattergl(
    #         x=nat_flow1.index,
    #         y=nat_flow1['stream depletion'],
    #         name = 'Stream Depletion',
    #         line = dict(color = colors1[1]),
    #         opacity = 0.8)

    #     # est_usage = go.Scattergl(
    #     #     x=nat_flow1.index,
    #     #     y=nat_flow1['estimated usage'],
    #     #     name = 'Estimated Stream Usage',
    #     #     line = dict(color = colors1[2]),
    #     #     opacity = 0.8)

    #     est_usage = go.Scattergl(
    #         x=nat_flow1.index,
    #         y=nat_flow1['allocation'],
    #         name = 'Allocation',
    #         line = dict(color = colors1[2]),
    #         opacity = 0.8)

    #     nat = go.Scattergl(
    #         x=nat_flow1.index,
    #         y=nat_flow1['nat flow'],
    #         name = 'Naturalised Flow',
    #         line = dict(color = colors1[0]),
    #         opacity = 0.8)

    #     data = [orig, meas_usage, est_usage, nat]

    #     layout = dict(
    #         title=input_site + ' Naturalisation',
    #         yaxis={'title': 'Flow rate (m3/s)'},
    #         dragmode='pan')

    #     config = {"displaylogo": False, 'scrollZoom': True, 'showLink': False}

    #     fig = dict(data=data, layout=layout)

    #     ## Save results
    #     # if hasattr(self, 'output_path'):
    #     #     run_time = pd.Timestamp.today().strftime('%Y-%m-%dT%H%M')

    #     #     nat_flow_html = outputs['nat_flow_html'].format(site=input_site, run_date=run_time)
    #     #     py.plot(fig, filename = os.path.join(self.output_path, nat_flow_html), config=config)
    #     # else:
    #     #     raise ValueError('plot must have an output_path set')

    #     return nat_flow1
