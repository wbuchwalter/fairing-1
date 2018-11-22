from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import abc 
import six

@six.add_metaclass(abc.ABCMeta)
class BuilderInterface(object):

    @abc.abstractmethod
    def execute(self, namespace, job_id, base_image):
        """Will be called when the build needs to start,
           This method should return a V1PodSpec with the correct image set.
           This is also where the builder should set the environment variables
           and volume/volumeMounts that it may need to work"""
        raise NotImplementedError('BuilderInterface.execute')
