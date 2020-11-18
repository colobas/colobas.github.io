<script>
  import BlinkingCursor from './BlinkingCursor.svelte';
  import { onMount } from 'svelte';

  export let content;
  export let text_size;

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  let displayed_content = "$ ";
  let total_len = 2 + content.length;
  $: pad_left = total_len - displayed_content.length;
  $: padding = (pad_left == 0 ? "":"x".repeat(pad_left-1));

  onMount (async () => {
    for (var ix = 0; ix < content.length; ix++) {
      await sleep((Math.random()+0.1)*300);
      displayed_content = displayed_content + content.charAt(ix);
    }
  });

</script>

<h1 style="--text-size: {text_size}" class="typewriter">
  {displayed_content}<BlinkingCursor></BlinkingCursor>
  <span id="padding">{padding}</span>
</h1>

<style>
    .typewriter{
      font-family: "IBM Px437";
      font-size: var(--text-size);
      display: inline-block;
      overflow-wrap: break-word;
      background-color: #000;
      color: #fff;
      margin-top: auto;
      margin-bottom: auto;
      padding: 0.2em;
      vertical-align: middle;
    }
    #padding{
      opacity: 0;
    }
</style>
