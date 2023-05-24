<template>
    <div>
        <video
        id="video-player"
        controls
        muted
        class="cld-video-player cld-video-player-skin-dark w-2/3 h-96 mx-auto"
        >
        </video>
        <p class="text-muted text-center text-sm">
            Placeholder by Max Andrey from Pexels
        </p>
    </div>
</template>

<script>

export default {
    async asyncData({ params }) {
        return {
            publicId: params.public_id
        };
    },

    data(){
        return {
            cld:null,
            player:null,
        };
    },

    mounted(){
        this.cld = cloudinary.Cloudinary.new({ cloud_name: process.env.NUXT_ENV_CLOUDINARY_CLOUD_NAME });

        this.player = this.cld.videoPlayer('video-player');

        this.player.source(
            {
                publicId: this.publicId,
                sourceTypes: ['hls'],
                format: 'm3u8',
            },
            {
                fluid: true,
                videojs: {
                    html5: {
                        hls: {overrideNative: true},
                        nativeAudioTracks: false,
                        nativeVideoTracks: false
                    },
                    loadingSpinner: false,
                },
                analytics: {
                    events: ['play', 'pause', 'ended', {type: 'percentsplayed', percents: [10, 40, 70, 90]}, 'error']
                },
                posterOptions: {
                    publicId: 'nuxtjs-webrtc-streaming/poster'
                }
            }
        );
    },
}
</script>
