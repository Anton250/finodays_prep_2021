<template>
  <v-container>
    <address-autocomplete v-model="address" />
    <v-row v-if="address">
      <v-col
        ><v-text-field
          label="Город"
          outlined
          disabled
          v-model="address.address.address.city"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          label="Улица"
          outlined
          disabled
          v-model="address.address.address.street"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          label="Дом"
          outlined
          disabled
          v-model="address.address.address.houseNumber"
        ></v-text-field
      ></v-col>
    </v-row>
    <v-row v-if="address">
      <v-col
        ><v-text-field
          label="Площадь"
          outlined
          v-model="priceForm.area"
          suffix="м.кв."
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          label="Количество комнат"
          outlined
          v-model="priceForm.rooms"
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          label="Этаж"
          outlined
          v-model="priceForm.level"
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          label="Количество этажей в доме"
          outlined
          v-model="priceForm.levels"
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-select
          :items="[
            { value: 0, text: 'Другое' },
            { value: 1, text: 'Панельный' },
            { value: 2, text: 'Монолитный' },
            { value: 3, text: 'Кирпичный' },
            { value: 4, text: 'Блочный' },
            { value: 5, text: 'Деревянный' },
          ]"
          label="Тип дома"
          item-text="text"
          item-value="value"
          v-model.number="priceForm.building_type"
          outlined
        ></v-select
      ></v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn
          v-if="address && Object.keys(priceForm).length >= 5"
          block
          color="primary"
          :loading="loading"
          @click="getPrice"
          >Рассчитать стоимость</v-btn
        >
      </v-col>
    </v-row>
    <v-row v-if="price">
      <v-col>
        <v-alert outlined type="success"
          >Рыночная стоимость квартиры: {{ numberWithCommas(price, " ") }} ₽</v-alert
        >
      </v-col>
      <v-col v-if="$store.state.settings.flat_discount != 0">
        <v-alert outlined type="info"
          >Дискаунт -{{ $store.state.settings.flat_discount }}%</v-alert
        >
      </v-col>
    </v-row>
    <v-row v-if="price">
      <v-col cols="12">
        <v-card>
          <v-card-subtitle>Итоговая стоимость</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <h3>{{numberWithCommas(Math.round(price * ((100 - $store.state.settings.flat_discount) / 100)), " ")}} ₽</h3>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AddressAutocomplete from "./AddressAutocomplete.vue";
import http from "../http";

export default {
  components: { AddressAutocomplete },
  data() {
    return {
      address: null,
      loading: false,
      flat: null,
      priceForm: {},
      price: null,
    };
  },
  methods: {
    async getFlat() {
      this.loading = true;
      let attributes = this.address.attributes;
      let filter = {
        macro_region_name: attributes.City,
        street: attributes.StreetName,
        street_type: attributes.Type,
        house: attributes.House,
        apartment: attributes.flat,
      };
      if (attributes.KorpusNumber) {
        filter.building = attributes.KorpusNumber;
      }
      let response = await http.getList("FlatByAddress", filter, true);
      this.flat = response.data;
      this.loading = false;
    },
    async getPrice() {
      this.loading = true;
      this.priceForm.geo_lat = this.address.geo.latitude;
      this.priceForm.geo_lon = this.address.geo.longitude;

      this.price = (
        await http.getList("FlarPrice", this.priceForm, true)
      ).data.price;
      this.loading = false;
    },
    numberWithCommas(x, sep) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep);
    },
  },
};
</script>

<style>
</style>