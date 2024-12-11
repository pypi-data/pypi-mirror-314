import threed_optix.package_utils.vars as v
import copy

class Beam:
    def __init__(self, power, rays_direction, wavelengths, appearance, source_type, num_of_rays, _part):
        self.power = power
        self.rays_direction = rays_direction
        self.wavelengths = wavelengths
        self.appearance = appearance
        self.source_type = source_type
        self.num_of_rays = num_of_rays
        self._part = _part
        return None

    def to_dict(self):
        return {
            'power': self.power,
            'angular_information': self.rays_direction,
            'wavelengths_data': self.wavelengths,
            'appearance_data': self.appearance,
            'source_type': self.source_type,
            'num_of_rays': self.num_of_rays
        }

    def copy(self):
        return copy.deepcopy(self)

class SimpleBeam(Beam):
    def __init__(self, power, rays_direction, wavelengths, appearance, source_type,num_of_rays, _part):
        super().__init__(power, rays_direction, wavelengths, appearance, source_type, num_of_rays, _part)
        return None

class PointSource(SimpleBeam):
    def __init__(self, power, rays_direction, wavelengths, appearance, spatial_information, num_of_rays, _part):
        super().__init__(power, rays_direction, wavelengths, appearance, v.POINT_SOURCE, num_of_rays, _part)
        self.spatial_information = spatial_information
        return None

    @classmethod
    def _new(cls,_part, _data):
        power = _data['power']
        rays_direction = _data['angular_information']
        wavelengths = _data['wavelengths_data']
        appearance = _data['appearance_data']
        spatial_information = _data['spatial_information']
        num_of_rays = _data['num_of_rays']
        return cls(power, rays_direction, wavelengths, appearance, spatial_information, num_of_rays, _part)

    def to_dict(self):
        beam_dict = super().to_dict()
        beam_dict['spatial_information'] = self.spatial_information
        return beam_dict

class PlaneWave(SimpleBeam):

    def __init__(self, power, rays_direction, wavelengths, appearance, spatial_information, num_of_rays, _part):
        super().__init__(power, rays_direction, wavelengths, appearance, v.PLANE_WAVE, num_of_rays, _part)
        self.spatial_information = spatial_information
        return None

    @classmethod
    def _new(cls, _part, _data):
        power = _data['power']
        rays_direction = _data['angular_information']
        wavelengths = _data['wavelengths_data']
        appearance = _data['appearance_data']
        spatial_information = _data['spatial_information']
        num_of_rays = _data['num_of_rays']

        return cls(power, rays_direction, wavelengths, appearance, spatial_information, num_of_rays, _part)

    def to_dict(self):
        beam_dict = super().to_dict()
        beam_dict['spatial_information'] = self.spatial_information
        return beam_dict

class GaussianBeam(Beam):
    def __init__(self, power, rays_direction, wavelengths, appearance, gaussian_beam, num_of_rays, _part):
        super().__init__(power, rays_direction, wavelengths, appearance, v.GAUSSIAN_BEAM, num_of_rays, _part)
        self.gaussian_beam = gaussian_beam
        return None

    @classmethod
    def _new(cls,_part, _data):
        power = _data['power']
        rays_direction = _data['angular_information']
        wavelengths = _data['wavelengths_data']
        appearance = _data['appearance_data']
        gaussian_beam = _data['gaussian_beam']
        num_of_rays = _data['num_of_rays']
        return cls(power, rays_direction, wavelengths, appearance, gaussian_beam, num_of_rays, _part)

    def to_dict(self):
        beam_dict = super().to_dict()
        beam_dict['gaussian_beam'] = self.gaussian_beam
        return beam_dict

def _create_beam(_part, _data):
    if _data['source_type'] == v.GAUSSIAN_BEAM:
        return GaussianBeam._new(_part, _data)
    elif _data['source_type'] == v.PLANE_WAVE:
        return PlaneWave._new(_part, _data)
    elif _data['source_type'] == v.POINT_SOURCE:
        return PointSource._new(_part, _data)
    else:
        raise Exception("Unknown source type")
