const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const config = {
    entry:  __dirname + '/frontend/reactapp.jsx',
    output: {
        path: __dirname + '/frontend/static/webbuild',
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.(jsx|js)?$/,
                loader: 'babel-loader',
                options: {
                    presets: ['react']
                },
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader',
                query: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.(woff2?|ttf|svg|eot)(\?v=\d+\.\d+\.\d+)?$/,
                loader: 'file-loader',
            }
        ]
    },
    plugins: [
        // new ExtractTextPlugin({
        //     filename: 'bundle.css',
        //     disable: false,
        //     allChunks: true
        // })
    ],
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
};
module.exports = config;