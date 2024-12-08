<!-- Wrapper around DocumentationAbsences.vue -->
<!-- That uses it either as list item or as editable modal dialog. -->
<template>
  <mobile-fullscreen-dialog v-model="popup" max-width="500px">
    <template #activator="activator">
      <!-- list view -> activate dialog -->
      <documentation-absences
        compact
        v-bind="$attrs"
        :extra-marks="extraMarks"
        :absence-reasons="absenceReasons"
        :dialog-activator="activator"
        :value="value"
        @input="$emit('input', $event)"
      />
    </template>
    <!-- dialog view -> deactivate dialog -->
    <!-- cancel | save (through lesson-summary) -->
    <documentation
      v-bind="$attrs"
      :extra-marks="extraMarks"
      :absence-reasons="absenceReasons"
      @close="popup = false"
    />
  </mobile-fullscreen-dialog>
</template>

<script>
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import DocumentationAbsences from "./DocumentationAbsences.vue";
import Documentation from "../documentation/Documentation.vue";

export default {
  name: "DocumentationAbsencesModal",
  components: {
    MobileFullscreenDialog,
    Documentation,
    DocumentationAbsences,
  },
  data() {
    return {
      popup: false,
    };
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
    extraMarks: {
      type: Array,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
};
</script>
