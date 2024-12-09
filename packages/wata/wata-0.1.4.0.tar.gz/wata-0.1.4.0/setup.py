from setuptools import setup, find_packages
import os
import sys

try:
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension

    TORCH = True
except:
    TORCH = False

'''
any: 适用于任何平台的通用版本。
manylinux1_x86_64: 适用于符合ManyLinux规范的x86_64 Linux系统。
win_amd64: 适用于64位Windows系统。
macosx_10_9_x86_64: 适用于OS X 10.9及以上版本的x86_64 Mac系统
'''


def make_cuda_ext(name, module, sources):
    # from torch.utils.cpp_extension import BuildExtension, CUDAExtension
    cuda_ext = CUDAExtension(
        name='%s.%s' % (module, name),
        sources=[os.path.join(*module.split('.'), src) for src in sources]
    )
    return cuda_ext


setupinfo = dict(
    name='wata',  # 包名
    version='0.1.4.0',  # 版本
    description="wangtao tools",  # 包简介
    platforms=['Linux','Windows','MacOS'],
    long_description=open('README.md', encoding='utf-8').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='wangtao',  # 作者
    author_email='1083719817@qq.com',  # 作者邮件
    maintainer='wangtao',  # 维护者
    maintainer_email='1083719817@qq.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    package_data={'': ['*.yaml', '*.txt', '*.bin', '*.pcd', '*.png', '*.ui',]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    options={
        'bdist_wheel': {
            'python_tag': 'py38',
            'plat_name': 'manylinux1_x86_64',
            'build_number': None,
            'dist_dir': None,
        }
    },
    python_requires='>=3.6',
    install_requires=['numpy',
                    #   'PyQt5',
                    #   'PyOpenGL',
                    #   'pyqtgraph',
                      'python-lzf',
                      'matplotlib',
                        # 'opencv-python==4.1.2.30',
                        # 'opencv-contrib-python',
                        # 'utm',
                      'tqdm', 
                      'utm',
                      'pyyaml', 'vtk', 'scipy',
                    #   'tabulate',
                      'pyquaternion'],
)

if sys.platform.startswith("linux") and TORCH == True:
    setup(
        name=setupinfo['name'],
        version=setupinfo['version'],
        description=setupinfo['description'],
        platforms=setupinfo['platforms'],
        long_description=setupinfo['long_description'],
        include_package_data=setupinfo['include_package_data'],
        author=setupinfo['author'],
        author_email=setupinfo['author_email'],
        maintainer=setupinfo['maintainer'],
        maintainer_email=setupinfo['maintainer_email'],
        license=setupinfo['license'],
        url=setupinfo['url'],
        packages=setupinfo['packages'],
        package_data=setupinfo['package_data'],
        classifiers=setupinfo['classifiers'],
        options=setupinfo['options'],
        python_requires=setupinfo['python_requires'],
        install_requires=setupinfo['install_requires'],
        cmdclass={'build_ext': BuildExtension, },
        ext_modules=[
            make_cuda_ext(
                name='roiaware_pool3d_cuda',
                module='wata.pointcloud.ops.roiaware_pool3d',
                sources=[
                    'src/roiaware_pool3d.cpp',
                    'src/roiaware_pool3d_kernel.cu',
                ]
            ),
        ],
    )

else:
    setup(
        name=setupinfo['name'],
        version=setupinfo['version'],
        description=setupinfo['description'],
        platforms=setupinfo['platforms'],
        long_description=setupinfo['long_description'],
        include_package_data=setupinfo['include_package_data'],
        author=setupinfo['author'],
        author_email=setupinfo['author_email'],
        maintainer=setupinfo['maintainer'],
        maintainer_email=setupinfo['maintainer_email'],
        license=setupinfo['license'],
        url=setupinfo['url'],
        packages=setupinfo['packages'],
        package_data=setupinfo['package_data'],
        classifiers=setupinfo['classifiers'],
        options=setupinfo['options'],
        python_requires=setupinfo['python_requires'],
        install_requires=setupinfo['install_requires'],
        # cmdclass=setupinfo['cmdclass'],
        # ext_modules=setupinfo['ext_modules'],
    )
