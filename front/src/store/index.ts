import Vue from 'vue'
import Vuex from 'vuex'
import { File } from '@/types/file'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    files: [] as File[],
  },
  mutations: {
    addFile({ files }, file: File) {
      files.push(file)
    },

    updateFile(state, { name, fields }) {
      state.files = state.files.map(f => (f.name === name ? { ...f, ...fields } : f))
    },
  },
  actions: {},
  modules: {},
})
