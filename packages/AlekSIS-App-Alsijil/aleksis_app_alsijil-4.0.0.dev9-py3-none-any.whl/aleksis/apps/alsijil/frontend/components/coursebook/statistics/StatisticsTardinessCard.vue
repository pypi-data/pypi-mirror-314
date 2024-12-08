<template>
  <v-skeleton-loader v-if="loading" type="card" />
  <v-card v-else>
    <v-card-text>
      <v-row>
        <v-col class="text-center">
          <div class="text-h2">
            {{ $n(tardinessCount) }}
          </div>
          <div class="text-subtitle-2">
            {{ $tc("alsijil.personal_notes.tardiness_n", tardinessCount) }}
          </div>
        </v-col>

        <v-col
          class="text-caption d-flex flex-column justify-center align-center"
        >
          <div>
            <div>
              <v-icon small>mdi-sigma</v-icon>
              {{ $tc("time.minutes_n", tardinessSum, { n: $n(tardinessSum) }) }}
            </div>
            <div>
              <v-icon small>mdi-diameter-variant</v-icon>
              {{
                $tc("time.minutes_n", tardinessSum / tardinessCount, {
                  n: $n(tardinessSum / tardinessCount),
                })
              }}
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "StatisticsTardinessCard",
  props: {
    tardinessSum: {
      type: Number,
      required: true,
    },
    tardinessCount: {
      type: Number,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>
