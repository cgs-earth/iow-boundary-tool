import { MapContainer } from 'react-leaflet';

import { MAP_CENTER, MAP_INITIAL_ZOOM } from '../constants';

export default function Map({ children }) {
    return (
        <MapContainer
            center={MAP_CENTER}
            zoom={MAP_INITIAL_ZOOM}
            zoomControl={false}
            style={{ height: '100vh' }}
        >
            {children}
        </MapContainer>
    );
}
