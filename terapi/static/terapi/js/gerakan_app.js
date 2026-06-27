const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            gerakanList: [],
            searchQuery: '',
            filterKategori: '',
            selectedGerakan: null,
            modalInstance: null
        }
    },
    computed: {
        filteredGerakan() {
            return this.gerakanList.filter(g => {
                const matchSearch = g.nama_gerakan.toLowerCase().includes(this.searchQuery.toLowerCase());
                const matchKategori = this.filterKategori ? g.kategori === this.filterKategori : true;
                return matchSearch && matchKategori;
            });
        }
    },
    methods: {
        async fetchGerakan() {
            try {
                const response = await axios.get('/terapi/api/gerakan/');
                this.gerakanList = response.data;
            } catch (error) {
                console.error("Error fetching gerakan:", error);
            }
        },
        showDetail(gerakan) {
            this.selectedGerakan = gerakan;
            if (!this.modalInstance) {
                this.modalInstance = new bootstrap.Modal(document.getElementById('detailModal'));
            }
            this.modalInstance.show();
        },
        youtubeEmbedUrl(url) {
            if (!url) return '';
            try {
                let videoId = '';
                if (url.includes('youtube.com/watch')) {
                    videoId = new URL(url).searchParams.get('v');
                } else if (url.includes('youtu.be/')) {
                    videoId = url.split('youtu.be/')[1].split('?')[0];
                }
                return `https://www.youtube.com/embed/${videoId}`;
            } catch (e) {
                return url;
            }
        }
    },
    mounted() {
        this.fetchGerakan();
    }
}).mount('#gerakanApp');
