<script>
</script>

<span class="blinking-cursor"><slot>█</slot></span>

<style>
    @-webkit-keyframes blinker {
      50% {
        opacity: 0.0;
      }
    }
    .blinking-cursor{
      -webkit-animation: blinker 1s step-start 0s infinite;
    }
</style>
