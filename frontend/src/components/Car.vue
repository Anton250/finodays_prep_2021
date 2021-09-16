<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-autocomplete
          v-model="brand"
          :items="brands"
          :loading="loadingBrands"
          hide-no-data
          hide-selected
          label="Марка"
          placeholder="Выберите марку"
          item-text="name"
          return-object
          clearable
        ></v-autocomplete>
        <v-autocomplete
          v-if="brand"
          v-model="model"
          :items="models"
          :loading="loadingModels"
          hide-no-data
          hide-selected
          label="Модель"
          placeholder="Выберите модель"
          item-text="name"
          return-object
          clearable
        ></v-autocomplete>
        <v-autocomplete
          v-if="model"
          v-model="generation"
          :items="generations"
          :loading="loadingGenerations"
          hide-no-data
          hide-selected
          label="Поколение"
          placeholder="Выберите поколение"
          item-text="name"
          return-object
          clearable
        ></v-autocomplete>
        <v-autocomplete
          v-if="generation"
          v-model="modification"
          :items="modifications"
          :loading="loadingModifications"
          hide-no-data
          hide-selected
          label="Модификация"
          placeholder="Выберите модификация"
          item-text="name"
          return-object
          clearable
        ></v-autocomplete
      ></v-col>
    </v-row>
    <v-row v-if="modification" class="mb-0 pb-0">
      <v-col
        ><v-text-field
          class="mb-0"
          label="Год"
          outlined
          v-model.number="priceForm.year"
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-select
          class="mb-0"
          :items="[
            { value: 0, text: 'Оригинал' },
            { value: 1, text: 'Дубликат' },
          ]"
          label="ПТС"
          item-text="text"
          item-value="value"
          v-model.number="priceForm.pts"
          outlined
        ></v-select>
      </v-col>
      <v-col
        ><v-text-field
          class="mb-0"
          label="Количество владельцев"
          outlined
          v-model="priceForm.owners_count"
          type="number"
        ></v-text-field
      ></v-col>
      <v-col
        ><v-text-field
          class="mb-0"
          label="Пробег"
          outlined
          v-model="priceForm.mileage"
          type="number"
        ></v-text-field
      ></v-col>
    </v-row>
    <v-row
      class="mt-0"
      v-if="modification && Object.keys(priceForm).length == 4"
    >
      <v-col>
        <v-btn @click="getPrice" :loading="loadingPrice" block color="primary"
          >Рассчитать стоимость</v-btn
        >
      </v-col>
    </v-row>
    <v-row v-if="price" class="my-0">
      <v-col cols="5">
        <v-alert outlined type="success"
          >Рыночная стоимость авто:
          {{ numberWithCommas(price, " ") }} ₽</v-alert
        >
      </v-col>
      <v-col>
        <v-alert :type="eco_classes[eco_class].type" outlined>
          Класс экологичности: {{ eco_classes[eco_class].name }}
          <span
            v-if="
              eco_class !== '' &&
              $store.state.settings.eco_class_coeffs[eco_class] != 1
            "
            >{{
              ($store.state.settings.eco_class_coeffs[eco_class] > 1
                ? "+"
                : "") +
              String(
                Math.round(
                  $store.state.settings.eco_class_coeffs[eco_class] * 100 - 100
                )
              )
            }}%</span
          >
        </v-alert>
      </v-col>
      <v-col v-if="$store.state.settings.car_discount != 0" cols="3">
        <v-alert outlined type="info"
          >Дискаунт -{{ $store.state.settings.car_discount }}%</v-alert
        >
      </v-col>
    </v-row>
    <v-row v-if="price" class="mt-0">
      <v-col cols="12">
        <v-card>
          <v-card-subtitle>Итоговая стоимость</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <h3>
                  {{
                    numberWithCommas(
                      Math.round(
                        price *
                          (((100 - $store.state.settings.car_discount) *
                            ($store.state.settings.eco_class_coeffs[
                              eco_class
                            ] || 1)) /
                            100)
                      ),
                      " "
                    )
                  }}
                  ₽
                </h3>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import http from "../http";
export default {
  data() {
    return {
      brand: null,
      model: null,
      generation: null,
      modification: null,
      loadingBrands: false,
      loadingModels: false,
      loadingGenerations: false,
      loadingModifications: false,
      loadingPrice: false,
      priceForm: {},
      price: null,
      eco_class: null,
      eco_classes: {
        electro: { name: "Электро", type: "success" },
        hybrid: { name: "Гибрид", type: "success" },
        euro1: { name: "Евро 1", type: "danger" },
        euro2: { name: "Евро 2", type: "danger" },
        euro3: { name: "Евро 3", type: "warning" },
        euro4: { name: "Евро 4", type: "warning" },
        euro5: { name: "Евро 5", type: "success" },
        euro6: { name: "Евро 6", type: "success" },
        "": { name: "Неизвестно", type: "info" },
      },
    };
  },
  methods: {
    async getPrice() {
      this.loadingPrice = true;
      let params = await http.getFilterValues(this.priceForm);
      let response = (
        await axios.get(
          `/rest_api/modification/${this.modification.id}/price/${params}`
        )
      ).data;
      this.price = response.price;
      this.eco_class = response.eco_class;
      this.loadingPrice = false;
    },
    numberWithCommas(x, sep) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep);
    },
  },
  computed: {
    brands() {
      return this.$store.state.brands;
    },
    models() {
      if (this.brand) {
        return this.$store.state.models[this.brand.id] || [];
      } else {
        return [];
      }
    },
    generations() {
      if (this.model) {
        return this.$store.state.generations[this.model.id] || [];
      } else {
        return [];
      }
    },
    modifications() {
      if (this.generation) {
        return this.$store.state.modifications[this.generation.id] || [];
      } else {
        return [];
      }
    },
  },
  watch: {
    async brand() {
      this.model = null;
      this.generation = null;
      this.modification = null;
      this.priceForm = {};
      this.price = null;
      if (!this.$store.state.models[this.brand.id]) {
        await this.$store.dispatch("getModels", this.brand.id);
      }
    },
    async model() {
      this.generation = null;
      this.modification = null;
      this.priceForm = {};
      this.price = null;
      if (!this.$store.state.generations[this.model.id]) {
        await this.$store.dispatch("getGenerations", this.model.id);
      }
    },
    async generation() {
      this.priceForm = {};
      this.price = null;
      if (!this.$store.state.modifications[this.generation.id]) {
        await this.$store.dispatch("getModifications", this.generation.id);
      }
    },
  },
  async beforeMount() {
    this.loadingBrands = true;
    await this.$store.dispatch("getBrands");
    this.loadingBrands = false;
  },
};
</script>

<style>
</style>