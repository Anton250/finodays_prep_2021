import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'

Vue.use(Vuex)

function sortItems(a, b) {
    if (a.name > b.name) {
        return 1;
    }
    if (a.name < b.name) {
        return -1;
    }
    // a должно быть равным b
    return 0;
}
function reversesortItems(a, b) {
    if (a.name < b.name) {
        return 1;
    }
    if (a.name > b.name) {
        return -1;
    }
    // a должно быть равным b
    return 0;
}

const store = new Vuex.Store({
    state: {
        user: null,
        isAuthenticated: false,
        brands: [],
        models: {},
        generations: {},
        modifications: {},
        settings: {},
    },
    getters: {},
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setSettings(state, settings) {
            state.settings = settings;
        },
        setBrands(state, brands) {
            brands.sort(sortItems);
            state.brands = brands;
        },
        setModels(state, { brand_id, models }) {
            models.sort(sortItems);
            Vue.set(state.models, brand_id, models);
        },
        setGenerations(state, { model_id, generations }) {
            generations.sort(reversesortItems);
            Vue.set(state.generations, model_id, generations);
        },
        setModifications(state, { generation_id, modifications }) {
            modifications.sort(sortItems);
            Vue.set(state.modifications, generation_id, modifications);
        },
    },
    actions: {
        async getBrands(context) {
            let brands = (await http.getList('Brand', {}, true)).data;
            context.commit('setBrands', brands);
        },
        async getModels(context, brand_id) {
            let models = (await http.getList('Model', { brand_id: brand_id }, true)).data;
            context.commit('setModels', { brand_id, models });
        },
        async getGenerations(context, model_id) {
            let generations = (await http.getList('Generation', { model_id: model_id }, true)).data;
            context.commit('setGenerations', { model_id, generations });
        },
        async getModifications(context, generation_id) {
            let modifications = (await http.getList('Modification', { generation_id: generation_id }, true)).data;
            context.commit('setModifications', { generation_id, modifications });
        },
        async getSettings(context) {
            let settings = (await http.getItem('Setting', 1, true)).data;
            context.commit('setSettings', settings);
        },
        async updateSettings(context, data) {
            let settings = (await http.updateItem('Setting', 1, data, true)).data;
            context.commit('setSettings', settings);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var username = creds.username;
            var password = creds.password;
            var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/
            var login_info = {
                email: username,
                password: password
            }
            if (username.match(reg_exp_mail) != null) {
                login_info = {
                    email: username,
                    password: password
                }
            } else {
                login_info = {
                    username: username,
                    password: password
                }
            }
            var status = false;
            try {
                await (Axios.post("/rest_api/auth/login/", login_info));
                status = true;
            } catch (error) {
                var data = error.response.data;
                if (data.non_field_errors) {
                    Vue.showErrorModal(data.non_field_errors);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            await Axios.post("/rest_api/auth/logout/");
            context.commit('setAuthenticated', false);
            context.commit('setUser', {});
        },
        async checkAuth(context) {
            try {
                var result = await Axios.get("/rest_api/auth/user/");
                if (result.status != 200) {
                    context.commit('setUser', {});
                    return
                }
                context.commit('setAuthenticated', true);
                context.commit('setUser', result.data);
            } catch (e) {
                context.commit('setUser', {});
            }
        },
    }
})

export default store;
