"""
Upload existing local media files to Cloudinary, preserving the relative paths
already stored in the database so no DB changes are required.

Usage:
    python manage.py migrate_media_to_cloudinary
    python manage.py migrate_media_to_cloudinary --dry-run
"""
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from lash_store.blog.models import BlogImage
from lash_store.product.models import ProductImages


class Command(BaseCommand):
    help = "Migrate locally-stored ImageField files to Cloudinary."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be uploaded without making API calls.",
        )

    def handle(self, *args, **options):
        import cloudinary
        import cloudinary.uploader

        if not cloudinary.config().cloud_name:
            raise CommandError(
                "Cloudinary is not configured. Set CLOUDINARY_URL in your .env first."
            )

        dry_run = options["dry_run"]
        media_root = settings.MEDIA_ROOT
        targets = [
            ("ProductImages", ProductImages.objects.all()),
            ("BlogImage", BlogImage.objects.all()),
        ]

        uploaded = 0
        skipped = 0
        missing = 0

        for label, queryset in targets:
            self.stdout.write(f"\n=== {label} ({queryset.count()} records) ===")
            for obj in queryset:
                relative_path = str(obj.image)
                if not relative_path:
                    skipped += 1
                    continue

                full_path = os.path.join(media_root, relative_path)
                if not os.path.isfile(full_path):
                    self.stdout.write(
                        self.style.WARNING(f"  MISSING  {relative_path}")
                    )
                    missing += 1
                    continue

                public_id = os.path.splitext(relative_path)[0]

                if dry_run:
                    self.stdout.write(f"  DRY-RUN  {relative_path}  ->  public_id={public_id}")
                    uploaded += 1
                    continue

                with open(full_path, "rb") as fh:
                    result = cloudinary.uploader.upload(
                        fh,
                        public_id=public_id,
                        overwrite=True,
                        resource_type="image",
                        use_filename=False,
                        unique_filename=False,
                    )
                self.stdout.write(self.style.SUCCESS(f"  OK       {relative_path}"))
                self.stdout.write(f"           {result['secure_url']}")
                uploaded += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done. uploaded={uploaded} missing={missing} skipped={skipped}"))
        if dry_run:
            self.stdout.write(self.style.NOTICE("(dry-run — no files were actually uploaded)"))
