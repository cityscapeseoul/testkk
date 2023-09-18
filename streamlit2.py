# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 17:05:38 2023

@author: seoul
"""
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from urllib.error import URLError

geo_data = 'bld_fczone_height.geojson'
import geopandas as gpd

df = gpd.read_file(geo_data)

# 좌표를 리스트로 변환하는 함수 정의
def multipolygon_to_list(multipolygon):
    coordinates_list = []
    for polygon in multipolygon.geoms:
        # Polygon 객체에서 좌표 추출 후 튜플을 리스트로 변환
        coordinates = [list(coord) for coord in polygon.exterior.coords]
        coordinates_list.extend(coordinates)  # extend를 사용하여 리스트에 추가
    return coordinates_list

# geometry 열을 수정하면서 새로운 열(coordinates) 추가
df['coordinates'] = df['geometry'].apply(multipolygon_to_list)

# Make layer
layer = pdk.Layer(
    'PolygonLayer', # 사용할 Layer 타입
    df, # 시각화에 쓰일 데이터프레임
    extruded=True,
    get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
    get_elevation="height2",
    elevation_scale=1.5,
    get_fill_color='[189, 211, 233, 225]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
    get_line_color='[255, 0, 0]',
    get_line_width=2,
    pickable=True, # 지도와 interactive 한 동작 on
    auto_highlight=True, # 마우스 오버(hover) 시 박스 출력,
    visible=True
)

layer_2d = pdk.Layer(
    'PolygonLayer', # 사용할 Layer 타입
    df, # 시각화에 쓰일 데이터프레임
    get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
    get_elevation="height2",
    get_fill_color='[189, 211, 233, 225]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
    get_line_color='[255, 0, 0]',
    get_line_width=2,
    pickable=True, # 지도와 interactive 한 동작 on
    auto_highlight=True, # 마우스 오버(hover) 시 박스 출력,
    visible=True
)

# Set the viewport location
center = [127.0509169, 37.5430332]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    pitch=45,
    bearing=30,
    zoom=14)


try:
    ALL_LAYERS = {
        "layer": pdk.Layer(
            'PolygonLayer', # 사용할 Layer 타입
            df, # 시각화에 쓰일 데이터프레임
            extruded=True,
            get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
            get_elevation="height2",
            elevation_scale=1.5,
            get_fill_color='[189, 211, 233, 225]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
            get_line_color='[255, 0, 0]',
            get_line_width=2,
            pickable=True, # 지도와 interactive 한 동작 on
            auto_highlight=True, # 마우스 오버(hover) 시 박스 출력,
            visible=True
        ),
        "layer_2d": pdk.Layer(
            'PolygonLayer', # 사용할 Layer 타입
            df, # 시각화에 쓰일 데이터프레임
            get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
            get_elevation="height2",
            get_fill_color='[189, 211, 233, 225]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
            get_line_color='[255, 0, 0]',
            get_line_width=2,
            pickable=True, # 지도와 interactive 한 동작 on
            auto_highlight=True, # 마우스 오버(hover) 시 박스 출력,
            visible=True
        ),
        
    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                initial_view_state=view_state,
                layers=selected_layers,
            ),
            use_container_width=True
        )
    else:
        st.error("Please choose at least one layer above.")

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )