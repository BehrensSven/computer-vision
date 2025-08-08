#!/usr/bin/env python3
"""
Dataset Download Script for Computer Vision Project

This script downloads the required datasets (GTSDB and LISA) for the project.
Run this script when setting up the project for the first time.

Usage:
    python scripts/download_datasets.py
"""

import sys
import zipfile
import tarfile
from pathlib import Path
import hashlib
import urllib.request
import subprocess
import shutil


class DatasetDownloader:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def download_file(self, url, destination, expected_hash=None):
        """Download a file with progress indication."""
        print(f"Downloading {url}...")
        
        try:
            urllib.request.urlretrieve(url, destination)
            print(f"Downloaded to {destination}")
            
            if expected_hash:
                if not self.verify_hash(destination, expected_hash):
                    raise ValueError(f"Hash verification failed for {destination}")
                    
        except Exception as e:
            print(f"Download failed: {e}")
            raise
                
    def verify_hash(self, filepath, expected_hash):
        """Verify file hash."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest() == expected_hash
        
    def extract_archive(self, archive_path, extract_to):
        """Extract zip or tar archive."""
        print(f"Extracting {archive_path}...")
        
        if archive_path.suffix.lower() == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_path.suffix.lower() in ['.tar', '.gz', '.tgz']:
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
        else:
            raise ValueError(f"Unsupported archive format: {archive_path.suffix}")
            
        print(f"Extracted to {extract_to}")
        
    def download_gtsdb(self):
        """Download German Traffic Sign Detection Benchmark."""
        gtsdb_dir = self.data_dir / "GTSDB"
        
        if gtsdb_dir.exists():
            print("GTSDB already exists, skipping download.")
            return
            
        print("=== Downloading GTSDB Dataset ===")
        
        # GTSDB Full IJCNN 2013 dataset
        url = "https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/FullIJCNN2013.zip"
        filename = "FullIJCNN2013.zip"
        filepath = self.data_dir / filename
        
        try:
            print("Downloading GTSDB Full IJCNN 2013 dataset (~2.7GB)...")
            print("This may take several minutes depending on your connection.")
            
            self.download_file(url, filepath)
            self.extract_archive(filepath, self.data_dir)
            
            # Clean up zip file
            filepath.unlink()
            print("GTSDB download and extraction completed!")
            
        except Exception as e:
            print(f"Error downloading GTSDB: {e}")
            print("You can manually download from:")
            print("https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/published-archive.html")
                
    def install_kagglehub(self):
        """Install kagglehub if not available."""
        try:
            import kagglehub
            return True
        except ImportError:
            print("kagglehub not found. Installing via pipx...")
            try:
                # Try pipx first with --include-deps
                subprocess.check_call(["pipx", "install", "kagglehub", "--include-deps"])
                return True
            except Exception as e1:
                print(f"pipx install failed: {e1}")
                try:
                    # Fallback to pip with --break-system-packages
                    print("Trying pip with --break-system-packages...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub", "--break-system-packages"])
                    import kagglehub
                    return True
                except Exception as e2:
                    print(f"Failed to install kagglehub: {e2}")
                    print("Please install manually:")
                    print("pipx install kagglehub --include-deps")
                    print("or: pip install kagglehub --break-system-packages")
                    return False
                
    def download_lisa(self):
        """Download LISA Traffic Sign Dataset from Kaggle."""
        lisa_dir = self.data_dir / "LISA"
        
        if lisa_dir.exists():
            print("LISA already exists, skipping download.")
            return
            
        print("=== Downloading LISA Dataset from Kaggle ===")
        
        if not self.install_kagglehub():
            print("Error: Could not install kagglehub.")
            print("Please install manually: pip install kagglehub")
            return
            
        try:
            import kagglehub
            
            print("Downloading LISA traffic light dataset from Kaggle...")
            print("This may take several minutes depending on your connection.")
            
            # Download dataset using kagglehub
            downloaded_path = kagglehub.dataset_download("mbornoe/lisa-traffic-light-dataset")
            print(f"Dataset downloaded to: {downloaded_path}")
            
            # Move or copy to our data directory
            downloaded_path = Path(downloaded_path)
            if downloaded_path.exists():
                if downloaded_path.is_dir():
                    shutil.copytree(downloaded_path, lisa_dir)
                else:
                    # If it's a single file, extract it
                    self.extract_archive(downloaded_path, lisa_dir)
                    
                print("LISA dataset setup completed!")
            else:
                print(f"Downloaded path {downloaded_path} not found.")
                
        except Exception as e:
            print(f"Error downloading LISA dataset: {e}")
            print("You can manually download from:")
            print("https://www.kaggle.com/datasets/mbornoe/lisa-traffic-light-dataset")
            print("Or use: kagglehub.dataset_download('mbornoe/lisa-traffic-light-dataset')")
            
    def create_readme(self):
        """Create README with dataset information."""
        readme_content = """# Datasets

This directory contains the computer vision datasets for this project.

## GTSDB (German Traffic Sign Detection Benchmark)
- Source: http://benchmark.ini.rub.de/
- Size: ~2.7GB
- Contains: German traffic sign images with annotations

## LISA (Laboratory for Intelligent & Safe Automobiles)
- Source: https://www.kaggle.com/datasets/mbornoe/lisa-traffic-light-dataset
- Size: ~4.9GB  
- Contains: US traffic sign images with annotations
- Downloaded via: kagglehub

## Setup
To download the datasets, run:
```bash
python scripts/download_datasets.py
```

Note: Some datasets require manual download due to license agreements.
"""
        
        readme_path = self.data_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
    def run(self):
        """Main download process."""
        print("Starting dataset download process...")
        print(f"Data directory: {self.data_dir.absolute()}")
        
        self.create_readme()
        
        # Download datasets
        self.download_gtsdb()
        self.download_lisa()
        
        print("\n=== Download Process Complete ===")
        print("Note: Some datasets may require manual download.")
        print("Check the README.md in the data/raw directory for details.")


if __name__ == "__main__":
    try:
        downloader = DatasetDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)