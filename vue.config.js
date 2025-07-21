const path = require("path");
const publicPath = process.env.NODE_ENV === "production" ? "./" : "/";
module.exports = {
  publicPath: publicPath,

  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
  },

  productionSourceMap: false,
};
