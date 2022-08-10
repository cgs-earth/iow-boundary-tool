import { MapContainer, TileLayer } from 'react-leaflet';

import { MAP_CENTER, MAP_INITIAL_ZOOM } from '../constants';

export default function Map() {
    return (
        <MapContainer
            center={MAP_CENTER}
            zoom={MAP_INITIAL_ZOOM}
            zoomControl={false}
            style={{ height: '100vh' }}
        >
            <TileLayer
                attribution='Powered by <a href="https://www.esri.com/">ESRI</a>'
                url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}.png'
            />
        </MapContainer>
    );
}
