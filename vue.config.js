const path = require("path");

module.exports = {
  publicPath: "/UmaE/",

  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
  },

  productionSourceMap: false,
};
