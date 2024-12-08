/**
 * Mixin to provide the cache update functionality used after creating or patching documentations
 */
export default {
  methods: {
    handleUpdateAfterCreateOrPatch(itemId) {
      return (cached, incoming) => {
        for (const object of incoming) {
          console.log("summary: handleUpdateAfterCreateOrPatch", object);
          // Replace the current documentation
          const index = cached.findIndex(
            (o) => o[itemId] === this.documentation.id,
          );
          // merged with the incoming partial documentation
          // if creation of proper documentation from dummy one, set ID of documentation currently being edited as oldID so that key in coursebook doesn't change
          cached[index] = {
            ...this.documentation,
            ...object,
            oldId:
              this.documentation.id !== object.id
                ? this.documentation.id
                : this.documentation.oldId,
          };
        }
        return cached;
      };
    },
  },
};
