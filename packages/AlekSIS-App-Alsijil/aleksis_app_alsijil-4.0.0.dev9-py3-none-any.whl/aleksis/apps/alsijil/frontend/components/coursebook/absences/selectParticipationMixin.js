/**
 * Mixin to provide passing through functionality for the events emitted when (de)selecting participations on the absence overview page
 */
export default {
  emits: ["select", "deselect"],
  methods: {
    handleSelect(participation) {
      this.$emit("select", participation);
    },
    handleDeselect(participation) {
      this.$emit("deselect", participation);
    },
  },

  computed: {
    /**
     * All necessary listeners bundled together to easily pass to child components
     * @returns {{select: Function, deselect: Function}}
     */
    selectListeners() {
      return {
        select: this.handleSelect,
        deselect: this.handleDeselect,
      };
    },
  },
};
