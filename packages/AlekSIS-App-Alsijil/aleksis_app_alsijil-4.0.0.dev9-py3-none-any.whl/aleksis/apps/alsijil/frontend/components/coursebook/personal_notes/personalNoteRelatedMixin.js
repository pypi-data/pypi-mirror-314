import documentationPartMixin from "../documentation/documentationPartMixin";

export default {
  mixins: [documentationPartMixin],
  props: {
    participation: {
      type: Object,
      required: true,
    },
  },
  computed: {
    personalNoteRelatedProps() {
      return {
        ...this.documentationPartProps,
        participation: this.participation,
      };
    },
  },
};
