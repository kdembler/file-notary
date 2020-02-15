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

    setFiles(state, files: FileInfo[]) {
      const newFiles = files.filter(f => !state.files.find(sf => sf.id === f.id))
      state.files = [...state.files, ...newFiles]
    },

    updateFile(state, { id, fields }) {
      state.files = state.files.map(f => (f.id === id ? { ...f, ...fields } : f))
    },
  },
  actions: {},
  modules: {},
})

export type RootStore = typeof store

export default store
