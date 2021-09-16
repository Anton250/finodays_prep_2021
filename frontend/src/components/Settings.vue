<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Настройки оценки автомобилей</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-subheader class="pl-0"> Дискаунт </v-subheader>
                <v-slider
                  v-model="settings.car_discount"
                  thumb-label="always"
                  :min="0"
                  :max="70"
                  :step="0.1"
                ></v-slider>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-expansion-panels>
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      Коэффициенты экологичности
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col
                          cols="6"
                          v-for="(item, name) in settings.eco_class_coeffs"
                          :key="name"
                        >
                          <v-subheader class="pl-0">
                            {{ eco_classes[name] }}
                          </v-subheader>
                          <v-slider
                            v-model="settings.eco_class_coeffs[name]"
                            thumb-label="always"
                            :min="0.5"
                            :max="1.5"
                            :step="0.01"
                          ></v-slider>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Настройки оценки квартир</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-subheader class="pl-0"> Дискаунт </v-subheader>
                <v-slider
                  v-model="settings.flat_discount"
                  thumb-label="always"
                  :min="0"
                  :max="50"
                  :step="0.1"
                ></v-slider>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn block color="primary" @click="updateSettings">Сохранить</v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar" color="green" timeout="1000">
      Данные успешно сохранены
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      eco_classes: {
        electro: "Электро",
        hybrid: "Гибрид",
        euro1: "Евро 1",
        euro2: "Евро 2",
        euro3: "Евро 3",
        euro4: "Евро 4",
        euro5: "Евро 5",
        euro6: "Евро 6",
      },
      snackbar: false,
    };
  },
  computed: {
    settings() {
      return { ...this.$store.state.settings };
    },
  },
  methods: {
    async updateSettings() {
      await this.$store.dispatch("updateSettings", this.settings);
      this.snackbar = true;
    },
  },
};
</script>

<style>
</style>