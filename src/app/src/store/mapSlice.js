import { createSlice } from '@reduxjs/toolkit';
import { DATA_LAYERS, MAP_INITIAL_ZOOM } from '../constants';

const initialState = {
    polygonIsVisible: true,
    addPolygonMode: false,
    editMode: false,
    layers: Object.keys(DATA_LAYERS),
    basemapType: 'default',
    geocodeResult: null,
    mapZoom: MAP_INITIAL_ZOOM,
};

export const mapSlice = createSlice({
    name: 'map',
    initialState,
    reducers: {
        togglePolygonVisibility: state => {
            state.polygonIsVisible = !state.polygonIsVisible;
        },
        startAddPolygon: state => {
            state.addPolygonMode = true;
        },
        cancelAddPolygon: state => {
            state.addPolygonMode = false;
        },
        toggleEditMode: state => {
            state.editMode = !state.editMode;
        },
        toggleLayer: (state, { payload: layerToToggle }) => {
            if (state.layers.includes(layerToToggle)) {
                state.layers = state.layers.filter(
                    layer => layer !== layerToToggle
                );
            } else {
                state.layers.push(layerToToggle);
            }
        },
        setBasemapType: (state, { payload: basemapType }) => {
            state.basemapType = basemapType;
        },
        setGeocodeResult: (state, { payload: result }) => {
            state.geocodeResult = result;
        },
        clearGeocodeResult: state => {
            state.geocodeResult = null;
        },
        setMapZoom: (state, { payload: mapZoom }) => {
            state.mapZoom = mapZoom;
        },
    },
});

export const {
    togglePolygonVisibility,
    startAddPolygon,
    cancelAddPolygon,
    toggleEditMode,
    toggleLayer,
    setBasemapType,
    setGeocodeResult,
    clearGeocodeResult,
    setMapZoom,
} = mapSlice.actions;

export default mapSlice.reducer;
