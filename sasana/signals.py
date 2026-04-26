from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Peserta, Instruktur, PengurusSasana, Sasana

@receiver([post_save, post_delete], sender=Peserta)
@receiver([post_save, post_delete], sender=Instruktur)
@receiver([post_save, post_delete], sender=PengurusSasana)
def invalidate_dashboard_stats(sender, instance, **kwargs):
    """Hapus cache statistik saat ada perubahan data peserta, instruktur, atau pengurus."""
    # Hapus cache daerah
    cache.delete('daerah_stats')
    
    # Hapus cache sasana spesifik jika ada
    if hasattr(instance, 'sasana') and instance.sasana:
        cache.delete(f'sasana_stats_{instance.sasana.id}')

@receiver([post_save, post_delete], sender=Sasana)
def invalidate_sasana_cache(sender, instance, **kwargs):
    """Hapus cache daerah jika sasana berubah."""
    cache.delete('daerah_stats')
