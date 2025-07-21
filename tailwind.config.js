module.exports = {
  purge: ["./src/App.vue", "./src/components/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: "class", // or 'media' or 'class'
  mode: "jit", // 是否开启 jit 模式，开启以后编译会更快，当然，tailwindcss 版本需要在 2.1 以上
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
