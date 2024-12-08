<template>
  <v-card :class="{ 'my-1 full-width': true, 'd-flex flex-column': !compact }">
    <v-card-title v-if="!compact">
      <lesson-information v-bind="documentationPartProps" />
    </v-card-title>

    <v-card-text
      class="full-width main-body"
      :class="{
        vertical: !compact || $vuetify.breakpoint.mobile,
        'pa-2': compact,
      }"
    >
      <lesson-information v-if="compact" v-bind="documentationPartProps" />

      <lesson-notes class="span-2" v-bind="documentationPartProps" />
      <participation-list
        v-if="documentation.canEditParticipationStatus"
        :include-present="false"
        class="participation-list"
        v-bind="documentationPartProps"
        :value="value"
        @input="$emit('input', $event)"
      />
    </v-card-text>
    <v-spacer />
    <v-divider />
    <v-card-actions v-if="!compact">
      <v-spacer />
      <cancel-button
        v-if="documentation.canEdit"
        @click="$emit('close')"
        :disabled="loading"
      />
      <save-button
        v-if="documentation.canEdit"
        @click="save"
        :loading="loading"
      />
      <cancel-button
        v-if="!documentation.canEdit"
        i18n-key="actions.close"
        @click="$emit('close')"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
import ParticipationList from "./ParticipationList.vue";
import LessonInformation from "../documentation/LessonInformation.vue";
import LessonNotes from "../documentation/LessonNotes.vue";

import SaveButton from "aleksis.core/components/generic/buttons/SaveButton.vue";
import CancelButton from "aleksis.core/components/generic/buttons/CancelButton.vue";

import { createOrUpdateDocumentations } from "../coursebook.graphql";

import documentationPartMixin from "../documentation/documentationPartMixin";

export default {
  name: "DocumentationAbsences",
  components: {
    ParticipationList,
    LessonInformation,
    LessonNotes,
    SaveButton,
    CancelButton,
  },
  emits: ["open", "close"],
  mixins: [documentationPartMixin],
  data() {
    return {
      loading: false,
      documentationsMutation: createOrUpdateDocumentations,
      selectedParticipations: [],
    };
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  methods: {
    save() {
      this.$refs.summary.save();
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.main-body {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: min-content min-content;
  column-gap: 1em;
}
.participation-list {
  grid-column-start: 1;
  grid-column-end: span 3;
}
.span-2 {
  grid-column-end: span 2;
}
.vertical > * {
  grid-column-end: span 3;
}
</style>
