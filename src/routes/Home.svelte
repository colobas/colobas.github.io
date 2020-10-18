<script>
import { onMount } from 'svelte'

import TwoCol from '../utils/TwoCol.svelte';
import BlinkingCursor from '../utils/BlinkingCursor.svelte';
import TypeTitle from '../utils/TypeTitle.svelte';
import CardTree from '../CardTree.svelte';

import MediaQuery from '../utils/MediaQuery.svelte';

let data = false;

onMount(async () => {
    const json_response = await fetch("/intro.json");
    data = await json_response.json();
});



</script>

<TwoCol>
  <span slot="left_content">
    <TypeTitle content="Hello, friend."></TypeTitle>
    <p id="bio">
    I'm Gui Pires.<br><br>
    * ML Engineer<br>
    * Lisbon -> Seattle<br>
    * Interested in tech, philosphy, politics, economics, books, food, and most
    importantly, saving the World.
    </p>
    <p id="links">
_____________________________________________________<br><br>
    <a href="https://github.com/colobas">
      <img class="icon" src="/iconmonstr-github-4.svg" alt="GitHub icon"></a> //
    <a href="https://twitter.com/colobas_">
      <img class="icon" src="/iconmonstr-twitter-4.svg" alt="Twitter icon"></a> //
     <a href="/cv.pdf">Curriculum Vitae</a><br>
    </p>

  </span>
  <span slot="right_content">
    <MediaQuery query="(min-width: 640px)" let:matches>
      {#if matches}
        {#if data}
          <CardTree data={data} />
        {/if}
      {/if}
    </MediaQuery>
    <MediaQuery query="(max-width: 640px)" let:matches>
      {#if matches}
        This website sucks on mobile, sorry... If you were on a desktop
      you'd be seeing a whole bunch of cool stuff here!!! :)
      {/if}
    </MediaQuery>
  </span>
</TwoCol>

<style>
  .icon { 
    -webkit-filter: invert(1);
            filter: invert(1);
    vertical-align: middle;
  }

  #bio {
    font-size: 20px;
  }

  #links {
    margin-top: 0;
  }

</style>
  
