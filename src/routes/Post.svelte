<script>
  import { onMount } from 'svelte'

  import TwoCol from '../utils/TwoCol.svelte';
  import BlinkingCursor from '../utils/BlinkingCursor.svelte';
  import TypeTitle from '../utils/TypeTitle.svelte';
  
  import CardTree from '../CardTree.svelte';
  import TextPost from '../TextPost.svelte';
  import MediaQuery from '../utils/MediaQuery.svelte';

  export let params;

  const json_root = "/json/";
  const html_root = "/html/";
  let data = false;
  let html_data = false;

  onMount(async () => {
      const json_response = await fetch(json_root + params.id + ".json");
      data = await json_response.json();

      const html_response = await fetch(html_root + params.id + ".html");
      html_data = await html_response.text();
  });

</script>

<TwoCol>
  <span slot="left_content">
    {#if data}
      {#if data.properties.title[0]}
      <TypeTitle content={data.properties.title[0]}></TypeTitle>
      {/if}
      <p>
      {#if data.properties.date.length > 0}
        Date: {data.properties.date[0]}<br>
      {/if}
        {#if data.properties.filetags.length > 0}
        Tags: 
        {#each data.properties.filetags as tag}
        #{tag+" "}
        {/each}
      {/if}
      </p>
      {#if data.properties.description.length > 0}
      <p>
        {data.properties.description[0]}
      </p>
      {/if}
    {/if}
  </span>
  <span slot="right_content">
    <MediaQuery query="(min-width: 640px)" let:matches>
      {#if matches}
        {#if params.type === "text"}
          <TextPost data={html_data} />
          <h1>this is a text post</h1>
        {:else if params.type === "tree"}
          {#if data}
          <CardTree data={data} />
          {/if}
        {:else}
          Something went wrong...
        {/if}
      {/if}
    </MediaQuery>
    <MediaQuery query="(max-width: 640px)" let:matches>
      {#if matches}
        <TextPost data={html_data} />
      {/if}
    </MediaQuery>
  </span>
</TwoCol>

<style>
</style>
  
