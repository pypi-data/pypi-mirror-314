
from ciocore.validator import Validator
from cioblender import assets
import logging
import bpy
from ciopath.gpath import Path

logger = logging.getLogger(__name__)
SAMPLES = 256

class ValidateScoutFrames(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        try:
            kwargs = self._submitter
            use_scout_frames = kwargs.get("use_scout_frames")
            scout_count = kwargs.get("scout_frames")
            chunk_size = kwargs.get("chunk_size")
            instance_type_name = kwargs.get("machine_type")

            if (not use_scout_frames or (use_scout_frames and scout_count == 0)) \
                and instance_type_name in ["best-fit-cpu", "best-fit-gpu"]:
                msg = (
                "We strongly recommend using Scout Frames with best fit instance types," +
                " as Conductor is not responsible for insufficient render nodes when using Best" +
                " Fit instance types."
                )
                self.add_warning(msg)

            if chunk_size > 1 and use_scout_frames:
                msg = "You have chunking set higher than 1."
                msg += " This can cause more scout frames to be rendered than you might expect."
                self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateScoutFrames: {}".format(e))
"""
class ValidateMAXSamples(Validator):
    def run(self, _):
        # Add a validation warning for a high Max Samples value
        try:
            scene = bpy.context.scene
            max_samples = scene.cycles.samples
            if max_samples > SAMPLES:
                msg = "You've increased the Max Samples beyond 256. "
                msg += "While having more samples generally improves results, "
                msg += "there's a point where the returns diminish. It's essential to perform test renders "
                msg += "to find the optimal sample count, balancing render time and quality. "
                msg += "Typically, a Max Samples value between 64 and 256, with Min Samples between 0 and 32 when using denoise, "
                msg += "suffices for most scenes. To adjust these settings, navigate to Render Properties > Sampling > Render."

                self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateResolvedChunkSize: {}".format(e))
"""
class ValidateResolvedChunkSize(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        try:
            kwargs = self._submitter
            chunk_size = kwargs.get("chunk_size", None)
            resolved_chunk_size = kwargs.get("resolved_chunk_size", None)
            if chunk_size and resolved_chunk_size:
                chunk_size = int(chunk_size)
                resolved_chunk_size = int(resolved_chunk_size)

                if resolved_chunk_size > chunk_size:
                    msg = "The number of frames per task has been automatically increased to maintain " \
                          "a total task count below 800. If you have a time-sensitive deadline and require each frame to be " \
                          "processed on a dedicated instance, you might want to consider dividing the frame range into smaller " \
                          "portions. " \
                          "Alternatively, feel free to reach out to Conductor Customer Support for assistance."
                    self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateResolvedChunkSize: {}".format(e))

class ValidateSaveSceneBeforeSubmission(Validator):
    def run(self, _):
        """
        Add a validation warning for a using CPU rendering with Eevee.
        """
        try:
            if bpy.data.is_dirty:
                msg = "The scene contains unsaved modifications. "
                msg += "To include these recent changes in your submission, select 'Save Scene and Continue Submission'. "
                msg += "Be aware that saving the scene now may result in additional upload time, "
                msg += "if the scene is already uploaded to the render farm. "
                msg += "If you prefer to proceed without incorporating these changes, choose 'Continue Submission'"
                self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateSaveSceneBeforeSubmission: {}".format(e))

class ValidateBaking(Validator):
    def run(self, _):
        """
        Check for a baking folder under modifiers then GeometryNodes then Simulation Bake Directory.
        If found, issue a warning about pausing the simulation and saving the scene before submitting the job.
        """
        try:
            # Iterate through all objects in the scene
            for obj in bpy.data.objects:
                # Check if the object has modifiers
                for modifier in obj.modifiers:
                    # Check if the modifier is a GeometryNodes modifier and has a simulation_bake_directory attribute
                    if modifier.type == 'NODES' and hasattr(modifier, 'simulation_bake_directory'):
                        msg = "Baking setup recognized. Please deactivate 'cache' from the simulation nodes and save the scene before submitting the job to Conductor."
                        self.add_warning(msg)
                        break  # Break out of the loop once the warning is added
        except Exception as e:
            logger.debug(f"ValidateBaking: {e}")


class ValidateGPURendering(Validator):
    def run(self, _):
        """
        Add a validation warning for a using CPU rendering with Eevee.
        """
        try:
            kwargs = self._submitter
            instance_type_family = kwargs.get("instance_type")
            driver_software = kwargs.get("render_software")
            if "eevee" in driver_software.lower() and "cpu" in instance_type_family.lower():
                msg = "CPU rendering is selected."
                msg += " We strongly recommend selecting GPU rendering when using Blender’s render engine, Eevee."
                self.add_warning(msg)
        except Exception as e:
            logger.debug("ValidateGPURendering: {}".format(e))


class ValidateFileAssetPathExclusion(Validator):
    def run(self, _):
        """
        Add a validation warning for file asset paths identified as home directories or root drives.
        """
        try:

            scene = bpy.context.scene
            rejected_file_assets = []

            # Check file assets
            for asset in scene.extra_file_assets_list:
                if asset.file_path and assets.is_home_directory_or_drive(asset.file_path):
                    rejected_file_assets.append(asset.file_path)
            # print("rejected_file_assets: ", rejected_file_assets)
            # Add warnings for rejected assets
            if rejected_file_assets:
                msg = f"File asset paths identified as home directories or root drives were not added. Please create a subfolder for:  {', '.join(rejected_file_assets)}"

                self.add_warning(msg)

        except Exception as e:
            logger.debug(f"ValidateFileAssetPathExclusion encountered an error: {e}")

class ValidateDirectoryAssetPathExclusion(Validator):
    def run(self, _):
        """
        Add a validation warning for asset paths identified as home directories or root drives.
        """
        try:

            scene = bpy.context.scene
            rejected_dir_assets = []

            # Check directory assets
            for asset in scene.extra_dir_assets_list:
                if asset.file_path and assets.is_home_directory_or_drive(asset.file_path):
                    rejected_dir_assets.append(asset.file_path)
            # print("rejected_dir_assets: ", rejected_dir_assets)
            if rejected_dir_assets:
                msg = f"Directory asset paths identified as home directories or root drives were not added. Please create a subfolder for: {', '.join(rejected_dir_assets)}"
                self.add_warning(msg)

        except Exception as e:
            logger.debug(f"ValidateDirectoryAssetPathExclusion encountered an error: {e}")

class ValidateFilePathSpaces(Validator):
    """
    Add a validation error for consecutive spaces in file path.
    """
    def run(self, _):
        try:
            file_name = bpy.data.filepath
            
            if "  " in file_name:
                    msg = ("Please remove all double spaces from the File Path ({})." \
                            " Double spaces will cause the render to fail.".format(file_name)
                        )
                    self.add_warning(msg)
            
        except Exception as e:
                logger.debug(f"ValidateFilePathSpaces encountered an error: {e}")

class ValidateOutputPathSpaces(Validator):
    def run(self, _):
        """
        Add a validation error for consecutive spaces in output path.
        """
        try:
            kwargs = self._submitter
            output_folder = kwargs.get("output_folder")
            
            if "  " in output_folder:
                msg = ("Please remove all double spaces from the Output Folder ({})." \
                        " Double spaces will cause the render to fail.".format(output_folder)
                    )
                self.add_warning(msg)
                
        except Exception as e:
            logger.debug(f"ValidateOutputPathSpaces encountered an error: {e}")

class ValidateRelativeOutputPath(Validator):
    def run(self, _):
        """
        Add a validation warning for relative output paths.
        """
        try:
            
            kwargs = self._submitter
            output_folder = kwargs.get("output_folder")
            
            if Path(output_folder).relative:
                msg = ("Please change your relative output path ({}) to " \
                        "an absolute path.".format(output_folder)
                    )
                self.add_error(msg)

        except Exception as e:
            logger.debug(f"ValidateRelativeOutputPath encountered an error: {e}")


class ValidateUploadDaemon(Validator):
    def run(self, _):
        try:
            scene = bpy.context.scene
            use_upload_daemon = scene.use_upload_daemon
            location = scene.location_tag
            if use_upload_daemon:
                if location is not None:
                    msg = "This submission expects an uploader daemon to be running and set to a specific location tag. "
                    msg += "Please make sure that you have installed ciocore from the Conductor Companion app "
                    msg += "and that you have started the daemon with the --location flag set to the same location tag."
                    msg += ' After you press continue you can open a shell and type: conductor uploader --location "{}"\n'.format(
                        location

                    )
                else:
                    msg = "This submission expects an uploader daemon to be running.\n"
                    msg += "Please make sure that you have installed ciocore from the Conductor Companion app "
                    msg += ' After you press continue, you can open a shell and type: "conductor uploader"'
                self.add_warning(msg)
        except Exception as e:
            print("Error in ValidateUploadDaemon:", str(e))

# Implement more validators here
####################################


def run(kwargs):
    errors, warnings, notices = [], [], []

    er, wn, nt = _run_validators(kwargs)

    errors.extend(er)
    warnings.extend(wn)
    notices.extend(nt)

    return errors, warnings, notices

def _run_validators(kwargs):


    validators = [plugin(kwargs) for plugin in Validator.plugins()]
    logger.debug("Validators: %s", validators)
    for validator in validators:
        validator.run(kwargs)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


