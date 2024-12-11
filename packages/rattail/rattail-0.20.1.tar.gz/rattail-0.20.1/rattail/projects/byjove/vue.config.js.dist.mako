// -*- mode: js; -*-

module.exports = {
    ## TODO: should get path from context
    publicPath: '/m/',
    devServer: {
        // host: '0.0.0.0',
        host: '127.0.0.1',
        ## TODO: should get port from context
        port: 7201,
        ## TODO: should get domain from context
        public: '${slug}-stage.example.com',
        // clientLogLevel: 'debug',
    }
}
