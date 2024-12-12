

import os
import tempfile
import logging
from pathlib import Path
from github import Github
from poly_hammer_utils.addon.packager import get_dict_from_python_file, zip_addon

logger = logging.getLogger(__name__)

class AddonRelease:
    def __init__(
            self, 
            github_token: str | None = None, 
            repo: str | None = None
        ):
        self.client = Github(login_or_token=github_token or os.environ['GH_PAT'])
        self.repo = self.client.get_repo(repo or os.environ['GITHUB_REPO'])


    def get_previous_releases(self) -> list[str]:
        """
        Gets the previous releases.

        Returns:
            list[str]: A list of the previous addon releases.
        """
        return [release.tag_name for release in self.repo.get_releases()]
    

    def delete_release(self, tag_name: str):
        """
        Deletes a release.
        
        Args:
            title (str): The title of the release to delete.
        """
        for release in self.repo.get_releases():
            if release.tag_name == tag_name:
                release.delete_release()
                logger.debug(f'Deleted release "{tag_name}"')


    def create_release(self, addon_folder: Path):
        """
        Creates a release for the addon if it doesn't exist already.

        Args:
            addon_folder (Path): The path to the addon folder.
        """
        addon_zip = zip_addon(
            addon_folder_path=addon_folder,
            output_folder=Path(tempfile.gettempdir()) / 'poly_hammer' / 'releases'
        )


        previous_releases = self.get_previous_releases()
        bl_info = get_dict_from_python_file(
            python_file=addon_folder / '__init__.py', 
            dict_name='bl_info'
        )
        title = bl_info['name']
        tag_name = '.'.join([str(i) for i in bl_info['version']])
        message = ''
        release_notes_path = addon_folder / 'release_notes.md'
        if release_notes_path.exists():
            with open(release_notes_path) as release_notes:
                message = release_notes.read()

        if tag_name not in previous_releases:
            logger.info(f'Creating release "{title}"')
            release = self.repo.create_git_release(
                name=title,
                message=message,
                tag=tag_name
            )

            logger.info(f'Uploading "{addon_zip}"')
            release.upload_asset(
                path=str(addon_zip),
                name=addon_zip.name,
                content_type='application/zip'
            )
        else:
            logger.warning(f'Release "{tag_name}" already exists!')
            self.delete_release(tag_name=tag_name)

            logger.info(f'Overwriting release "{title}"')
            release = self.repo.create_git_release(
                name=title,
                message=message,
                tag=tag_name
            )

            logger.info(f'Uploading "{addon_zip}"')
            release.upload_asset(
                path=str(addon_zip),
                name=addon_zip.name,
                content_type='application/zip'
            )
        
        logger.info('Successfully released!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    AddonRelease().create_release(addon_folder=Path(os.environ['ADDON_FOLDER']))