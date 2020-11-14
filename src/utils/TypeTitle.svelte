<script>
  import BlinkingCursor from './BlinkingCursor.svelte';
  import { onMount } from 'svelte';

  export let content;

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  let displayed_content = "$ ";
  $: padding = "x".repeat((content.length + 2) - displayed_content.length);

  onMount (async () => {
    for (var ix = 0; ix < content.length; ix++) {
      await sleep((Math.random()+0.1)*300);
      displayed_content = displayed_content + content.charAt(ix);
    }
  });

</script>

<h1 class="typewriter">
  {displayed_content}<BlinkingCursor></BlinkingCursor>
  <span id="padding">{padding}</span>
</h1>

<style>
    .typewriter{
      font-family: "IBM Px437";
      display: inline-block;
      overflow-wrap: break-word;
    }
    #padding{
      opacity: 0;
    }
</style>
