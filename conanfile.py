from json import tool
from conans import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps
from conan.tools.layout import cmake_layout
import os

class Emf4cppConan(ConanFile):
    name = "emf4cpp"
    version = "2.1.0"
    license = "LGPL-3.0-or-later"
    author = "Cátedra SAES-UMU", "RamakrishnanOSS"
    url = "https://github.com/RamakrishnanOSS/emf4cpp"
    description = " C++ implementation and type mapping for the Eclipse Modeling Framework"
    topics = ("Eclipse", "EMF")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports = [ 
        "emf4cpp/*",
        "emf4cpp.tests/*",
        "emf4cpp.xtext/*", 
        "emf4cpp.xtext2qi/*", 
        "org.csu.emf4cpp.generator/*", 
        "org.csu.emf4cpp.plugin/*", 
        "CMakeLists.txt"
    ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def package(self):
        cmake = CMake(self)
        cmake.install()
        # in order to offer a header inclusion without emf4cpp namespace
        os.symlink( 
            os.path.join(self.package_folder,"include","emf4cpp","ecorecpp"),
            os.path.join(self.package_folder,"include","ecorecpp")
        )
        os.symlink( 
            os.path.join(self.package_folder,"include","emf4cpp","ecore"),
            os.path.join(self.package_folder,"include","ecore")
        )
        os.symlink( 
            os.path.join(self.package_folder,"include","emf4cpp","ecorecpp.hpp"),
            os.path.join(self.package_folder,"include","ecorecpp.hpp")
        )
        os.symlink( 
            os.path.join(self.package_folder,"include","emf4cpp","ecore_forward.hpp"),
            os.path.join(self.package_folder,"include","ecore_forward.hpp")
        )
        os.symlink( 
            os.path.join(self.package_folder,"include","emf4cpp","ecore.hpp"),
            os.path.join(self.package_folder,"include","ecore.hpp")
        )
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

