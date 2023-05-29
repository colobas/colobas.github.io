import BlinkingCursor from './BlinkingCursor.svelte';
import TypeTitle from './TypeTitle.svelte';

new TypeTitle({
  target: document.querySelector('#hello-friend'),
  props: {
    content: "Hello friend"
  }
});
