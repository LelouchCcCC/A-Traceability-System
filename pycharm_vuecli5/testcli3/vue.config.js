const {defineConfig} = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
    transpileDependencies: true,
    configureWebpack: {
        resolve: {
            alias: {
                'assets': '@/assets',
                'common': '@/common',
                'components': '@/components',
                'network': '@/network',
                // 'assets':'@/assets',
            }
        },
    },
})
