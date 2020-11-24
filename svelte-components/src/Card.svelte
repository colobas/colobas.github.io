<script>
  import marked from 'marked';

  export let key;
  export let body;
  export let color;
  export let _class;

</script>

<div class="{_class}" style="background-color: {color}">
{#if key != "raw"}
  {#if key != ",,,,blank,,,,"}
    <h2>{key}</h2>
  {/if}
  {#if body.raw}
    {@html marked(body.raw)}
  {/if}
{:else if key == "raw"}
  {@html marked(body)}
{/if}
</div>

<style>
.card {
  display: block;
  border: solid black;
  margin: 1em;
  padding: 0.2em 1em 1em 1em;
  text-size: 20px;
  border-width: 1px;
  color: white;
}

:global(img) {
  max-width: 90%;
  margin: auto;
}

.highlighted {
  border-width: 5px;
  border: solid red;
}
h2 {
  margin-top: 0.5em;
}

h2 a {
  color: #fff;
  text-decoration: underline;
}
 
</style>
