<!-- Wrapper around Documentation.vue -->
<!-- That uses it either as list item or as editable modal dialog. -->
<template>
  <mobile-fullscreen-dialog
    v-model="popup"
    max-width="500px"
    :persistent="dirty"
  >
    <template #activator="activator">
      <!-- list view -> activate dialog -->
      <documentation
        compact
        v-bind="$attrs"
        :dialog-activator="activator"
        :extra-marks="extraMarks"
        :absence-reasons="absenceReasons"
        :subjects="subjects"
      />
    </template>
    <!-- dialog view -> deactivate dialog -->
    <!-- cancel | save (through lesson-summary) -->
    <documentation
      v-bind="$attrs"
      :extra-marks="extraMarks"
      :absence-reasons="absenceReasons"
      :subjects="subjects"
      @close="popup = false"
      @dirty="dirty = $event"
    />
  </mobile-fullscreen-dialog>
</template>

<script>
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import Documentation from "./Documentation.vue";

export default {
  name: "DocumentationModal",
  components: {
    MobileFullscreenDialog,
    Documentation,
  },
  data() {
    return {
      popup: false,
      dirty: false,
    };
  },
  props: {
    extraMarks: {
      type: Array,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
    subjects: {
      type: Array,
      required: true,
    },
  },
};
</script>
