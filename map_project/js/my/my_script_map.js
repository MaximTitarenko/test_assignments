var map = L.map('map',{center: [47.24010, 39.71067], zoom: 17});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// добавление точек интереса
var runIcon = L.icon({
    iconUrl: 'img/map_icons/ico_run_300.png',
    iconSize: [50, 50], // size of the icon
    });

var marker = L.marker([47.24070, 39.70950], {icon: runIcon}).bindPopup('Легкоатлетический манеж ДГТУ').addTo(map);

var swimIcon = L.icon({
    iconUrl: 'img/map_icons/ico_swim_300.png',
    iconSize: [50, 50], // size of the icon
    });

var marker = L.marker([47.23875, 39.71094], {icon: swimIcon}).bindPopup('Бассейн "Универ"').addTo(map);

var sqrlIcon = L.icon({
    iconUrl: 'img/map_icons/ico_squirrel_300.png',
    iconSize: [50, 50], // size of the icon
    });

var marker = L.marker([47.24217, 39.71154], {icon: sqrlIcon}).bindPopup('Белки').addTo(map);

// подключение плагинов
L.control.mousePosition().addTo(map);
L.Control.measureControl().addTo(map);