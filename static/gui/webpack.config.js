var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: './static/js/main.js',
    watch: true,
    output: {
        path: path.resolve(__dirname, './static/build'),
        filename: 'app.bundle.js'
    },
    module: {
        rules: [ // Changed from "loaders" to "rules" which is the Webpack 2+ syntax
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'], // Use the updated presets here
                        cacheDirectory: true
                    }
                }
            },
        ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map'
};
