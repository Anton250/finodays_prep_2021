<template>
  <div>
    <v-autocomplete
      v-model="selected"
      :items="matches"
      :loading="loading"
      :search-input.sync="searchQuery"
      hide-no-data
      hide-selected
      label="Адрес"
      placeholder="Введите адрес"
      prepend-icon="location_on"
      item-text="show_label"
      return-object
      no-filter
      clearable
    >
      <template v-slot:item="data">
        <span v-html="data.item.label"></span>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
import Axios from "axios";
import _ from "lodash";

export default {
  props: ["value"],
  data() {
    return {
      searchQuery: "",
      matches: [],
      selected: this.value,
      loading: false,
      apiKey: "78bhiTliLYkKcCMilhXup8uJVRnoWcMvJaVJbFNOWrA",
    };
  },
  watch: {
    searchQuery() {
      if (this.searchQuery) {
        this.fetchAddresses(this.searchQuery, this);
      }
    },
    async selected() {
      if (this.selected) {
        for (let key in this.selected.address) {
          this.selected.address[key] = this.selected.address[key]
            .replaceAll("<span class=highlighted>", "")
            .replaceAll("</span>", "");
        }
        let data = {
          address: this.selected,
        };
        let response = await Axios.get(
          `https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey=${this.apiKey}&locationid=${this.selected.locationId}&jsonattributes=1&gen=9`
        );
        data.geo = response.data.response.view[0].result[0].location.navigationPosition[0];
        this.$emit("input", data);
      }
    },
  },
  methods: {
    fetchAddresses: _.debounce(async (search, vue) => {
      vue.loading = true;
      let response = await Axios.get(
        `https://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json?apiKey=${
          vue.apiKey
        }&country=RUS&language=ru&query=${search.replaceAll(
          " ",
          "+"
        )}&beginHighlight=<span class%3Dhighlighted>&endHighlight=</span>`
      );
      // let response = await Axios.get(
      //   `https://pkk.rosreestr.ru/arcgis/rest/services/Address/pkk_locator_street/GeocodeServer/findAddressCandidates?SingleLine=${search.replaceAll(
      //     " ",
      //     "+"
      //   )}&OBJECTID=0&outFields=*&f=json`
      // );
      let data = [];
      for (let suggestion of response.data.suggestions) {
        suggestion.show_label = suggestion.label
          .replaceAll("<span class=highlighted>", "")
          .replaceAll("</span>", "");
        data.push(suggestion);
      }
      vue.matches = data;
      vue.loading = false;
    }, 300),
  },
};
</script>

<style>
.highlighted {
  background-color: lightgrey;
}
</style>