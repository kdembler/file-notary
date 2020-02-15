import Vue from 'vue'
import Vuex from 'vuex'
import { FileInfo } from '@/types/fileInfo'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    files: [] as FileInfo[],
  },
  mutations: {
    addFile({ files }, file: FileInfo) {
      files.push(file)
    },

    setFiles({ files }, newFiles: FileInfo[]) {
      files = newFiles
    },

    // updateFile(state, { name, fields }) {
    //   state.files = state.files.map(f => (f.name === name ? { ...f, ...fields } : f))
    // },
  },
  actions: {},
  modules: {},
})

export type RootStore = typeof store

export default store
