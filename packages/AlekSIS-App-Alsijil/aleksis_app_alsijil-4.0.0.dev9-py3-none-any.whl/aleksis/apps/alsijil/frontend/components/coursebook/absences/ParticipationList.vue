<script setup>
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
</script>

<template>
  <v-list v-if="filteredParticipations.length">
    <v-divider />

    <v-list-item-group :value="value" multiple @change="changeSelect">
      <template v-for="(participation, index) in filteredParticipations">
        <v-list-item
          :key="`documentation-${documentation.id}-participation-${participation.id}`"
          :value="participation.id"
          v-bind="$attrs"
          two-line
        >
          <template #default="{ active }">
            <v-list-item-action>
              <v-checkbox :input-value="active" />
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ participation.person.fullName }}
              </v-list-item-title>
              <absence-reason-group-select
                v-if="participation.absenceReason && !compact"
                class="full-width"
                allow-empty
                :load-selected-chip="loading"
                :custom-absence-reasons="absenceReasons"
                :value="participation.absenceReason?.id || 'present'"
                @input="sendToServer([participation], 'absenceReason', $event)"
              />
            </v-list-item-content>
            <v-list-item-action v-if="participation.absenceReason && compact">
              <absence-reason-group-select
                allow-empty
                :load-selected-chip="loading"
                :custom-absence-reasons="absenceReasons"
                :value="participation.absenceReason?.id || 'present'"
                @input="sendToServer([participation], 'absenceReason', $event)"
              />
            </v-list-item-action>
          </template>
        </v-list-item>
        <v-divider
          v-if="index < filteredParticipations.length - 1"
          :key="index"
        ></v-divider>
      </template>
    </v-list-item-group>
  </v-list>
</template>

<script>
import updateParticipationMixin from "./updateParticipationMixin";

export default {
  name: "ParticipationList",
  mixins: [updateParticipationMixin],
  data() {
    return {
      loading: false,
      participationDialogs: false,
      isExpanded: false,
    };
  },
  props: {
    includePresent: {
      type: Boolean,
      required: false,
      default: true,
    },
    value: {
      type: Array,
      required: true,
    },
  },
  computed: {
    filteredParticipations() {
      if (!this.includePresent) {
        return this.documentation.participations.filter(
          (p) => !!p.absenceReason,
        );
      } else {
        return this.documentation.participations;
      }
    },
  },
  methods: {
    changeSelect(value) {
      this.$emit("input", value);
    },
  },
};
</script>
