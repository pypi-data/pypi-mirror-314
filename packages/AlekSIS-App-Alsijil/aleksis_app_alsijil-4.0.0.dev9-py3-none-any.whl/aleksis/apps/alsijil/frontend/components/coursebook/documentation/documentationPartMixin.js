/**
 * Mixin to provide common fields for all components specific to a singular documentation inside the coursebook
 */
export default {
  props: {
    /**
     * The documentation in question
     */
    documentation: {
      type: Object,
      required: true,
    },
    /**
     * The query used by the coursebook. Used to update the store when data changes.
     */
    affectedQuery: {
      type: Object,
      required: true,
    },
    /**
     * Whether the documentation is currently in the compact mode (meaning coursebook row)
     */
    compact: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * Activator attributes and event listeners to open documentation dialog in different places
     */
    dialogActivator: {
      type: Object,
      required: false,
      default: () => ({ attrs: {}, on: {} }),
    },
    /**
     * Once loaded list of all extra marks to avoid excessive network and database queries
     */
    extraMarks: {
      type: Array,
      required: true,
    },
    /**
     * Once loaded list of absence reasons to avoid excessive network and database queries
     */
    absenceReasons: {
      type: Array,
      required: true,
    },
    /**
     * Once loaded list of subjects to avoid excessive network and database queries
     */
    subjects: {
      type: Array,
      required: true,
    },
  },

  computed: {
    /**
     * All necessary props bundled together to easily pass to child components
     * @returns {{compact: Boolean, documentation: Object, dialogActivator: Object<{attrs: Object, on: Object}>}}
     */
    documentationPartProps() {
      return {
        documentation: this.documentation,
        compact: this.compact,
        dialogActivator: this.dialogActivator,
        affectedQuery: this.affectedQuery,
        extraMarks: this.extraMarks,
        absenceReasons: this.absenceReasons,
        subjects: this.subjects,
      };
    },
  },
};
