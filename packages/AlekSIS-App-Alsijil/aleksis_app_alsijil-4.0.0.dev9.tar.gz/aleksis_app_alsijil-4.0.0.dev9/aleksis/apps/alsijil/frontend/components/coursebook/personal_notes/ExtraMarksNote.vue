<script>
import ExtraMarkNoteCheckbox from "./ExtraMarkNoteCheckbox.vue";
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";

export default {
  name: "ExtraMarksNote",
  components: { ExtraMarkNoteCheckbox },
  mixins: [personalNoteRelatedMixin],
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
};
</script>

<template>
  <div>
    <extra-mark-note-checkbox
      v-for="extraMark in extraMarks"
      :key="'checkbox-extramark-' + extraMark.id"
      v-bind="{ ...personalNoteRelatedProps, ...$attrs }"
      :value="extraMark"
      :personal-note="value.find((pn) => pn.extraMark.id === extraMark.id)"
    />
  </div>
</template>
