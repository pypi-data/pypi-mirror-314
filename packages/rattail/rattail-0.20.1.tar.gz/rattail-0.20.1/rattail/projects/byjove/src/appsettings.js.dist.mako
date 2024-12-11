## -*- coding: utf-8; mode: js; -*-

import packageData from "../package.json"

var appsettings = {
    systemTitle: "${system_name}",
    appTitle: "${name}",
    version: packageData.version,
    logo: '/Hymenocephalus_italicus.jpg',
    production: false,
    watermark: 'url("/tailbone/img/testing.png")',
};

export default appsettings;
