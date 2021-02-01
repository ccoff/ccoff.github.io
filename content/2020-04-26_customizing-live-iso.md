Title: Customizing a live ISO image
Category: blog
Tags: linux, iso, live image
Slug: customizing-live-iso-image
Date: 2020-04-26

I have an [Atomic Pi](https://www.digital-loggers.com/api_faqs.html) that I use as a NAS. Every now and then, I back up the on-board eMMC with *dd*. To do this, I boot from a [live Debian image](https://www.debian.org/CD/live) on a USB stick. This requires attaching a keyboard and monitor to the normally headless server, though -- the live image waits for a keypress at the boot menu, and it doesn't start an SSH server. So there is no way to access it remotely.

I wanted to be able to plug in the live USB stick, boot the server, connect via SSH, and *dd* the eMMC without having to connect other hardware. As it turns out, modifying the filesystem of a live ISO image is not difficult. The following procedure shows how to take a Debian live ISO file, unpack it, modify the filesystem, and pack it back up into a new, customized ISO file.

First, we create some working directories where we can extract and modify the ISO image:

```text
mkdir -p custom-iso/mnt
mkdir -p custom-iso/iso
mkdir -p custom-iso/squashfs
```

Next, we mount the Debian ISO image file to get to the files inside. (Below, it's mounted at */media/d-live 10.4.0 st amd64*.) We use *rsync* to copy the files from there into the *custom-iso/iso* directory. After that, we mount the ISO file's squashfs filesystem in the *custom-iso/mnt* directory, and finally copy the unpacked contents of the squashed filesystem into the *custom-iso/squashfs* directory:

```text
cd custom-iso
sudo rsync -a /media/d-live\ 10.4.0\ st\ amd64/ iso/
sudo mount -o loop iso/live/filesystem.squashfs mnt
sudo rsync -a mnt/ squashfs/
```

We have the squash filesystem extracted, and we're ready to modify it. Before we enter a chroot to do that though, let's copy the current *resolv.conf* to make sure networking works correctly:

```text
sudo cp /etc/resolv.conf squashfs/etc
```

Now we can enter the chroot:

```text
sudo chroot ./squashfs
```

We can make any changes we like in here. The following commands install an SSH server, configure it, and clean up. Remember, this is all done *inside* the chroot:

```text
mount -t proc none /proc/
mount -t sysfs none /sys/

apt update
apt install openssh-server

# Set a root password:
passwd

# Add a regular user for SSH logins:
sudo adduser sshuser

# Configure sshd_config, make any other configuration changes here, etc.

# Clean up after ourselves:
apt clean
rm -rf /tmp/*
umount /proc/
umount /sys/
 rm ~/.bash_history
 exit
```

(Note the leading space before the last two commands -- this ensures Bash doesn't save the commands in its history.)

At this point, we've modified the filesystem to what we want, but we still need to make a few more tweaks to the live configuration. The default Debian live ISO waits for the user to select an option during startup -- obviously that's a problem in a headless environment. We want the image to boot automatically with no intervention so we can get the all-important SSH server running. So we edit the *iso/boot/grub/grub.cfg* file, and set a timeout (2 seconds here) for the boot menu:

```text
set timeout=2
```

We want to cover EFI and isolinux boot environments, so we edit the *iso/isolinux/isolinux.cfg* file as well (here the time is specified in deciseconds):

```text
timeout 20
```

That's it for the modifications. Now we're ready to build a new ISO file with our changes in it. First we need to install a few packages:

```text
sudo apt install xorriso
sudo apt install isolinux
sudo apt install squashfs-tools
```

Next we "re-squash" the filesystem and copy it back into the *iso/live* directory:

```text
sudo mksquashfs squashfs filesystem.squashfs
cp filesystem.squashfs iso/live
```

And finally, we build the new ISO file with the following lovely one-liner... We can change the **-outdev** and **-volid** options to whatever names we want for the filename and volume name:

```text
xorriso -outdev debian-live-10.4.0-amd64-custom.iso -volid d-live\ 10.4\ cust\ amd64 -padding 0 \
-compliance no_emul_toc -map ./iso / -chmod 0755 / -- -boot_image isolinux dir=/isolinux \
-boot_image isolinux system_area=/usr/lib/ISOLINUX/isohdpfx.bin -boot_image any next \
-boot_image any efi_path=boot/grub/efi.img -boot_image isolinux partition_entry=gpt_basdat
```

When that command finishes, we have a customized ISO file suitable for a USB drive, CD, or other boot media. Making disk image backups on a headless device is a lot easier now.

