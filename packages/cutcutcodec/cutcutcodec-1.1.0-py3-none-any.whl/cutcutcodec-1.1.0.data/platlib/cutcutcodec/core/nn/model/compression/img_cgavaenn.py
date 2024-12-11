#!/usr/bin/env python3

"""Implement a convolutive generative adversarial variational auto-encoder neuronal network."""

import lightning
import torch


class VariationalEncoder(torch.nn.Module):
    """Projects images into a more compact space.

    Each patch of 192x192 pixels with a stride of 32 pixels
    is projected into a space of dimension 256.
    """

    def __init__(self):
        super().__init__()

        eta = 1.605  # (lat_dim/first_dim)**(1/nb_layers)

        self.pre = torch.nn.Sequential(
            torch.nn.Conv2d(3, 24, kernel_size=3),
            torch.nn.ELU(),
        )
        self.encoder = torch.nn.Sequential(
            *(
                torch.nn.Sequential(
                    torch.nn.Conv2d(
                        round(24*eta**layer),
                        round(24*eta**(layer+1)),
                        kernel_size=5,
                        stride=2,
                        padding=2,
                        bias=False,
                    ),
                    torch.nn.BatchNorm2d(round(24*eta**(layer+1))),
                    torch.nn.ELU(),
                    torch.nn.Dropout(0.1),
                    torch.nn.Conv2d(
                        round(24*eta**(layer+1)),
                        round(24*eta**(layer+1)),
                        kernel_size=3,
                    ),
                    torch.nn.ELU(),
                    torch.nn.Dropout(0.1),
                )
                for layer in range(5)
            ),
        )
        self.post = torch.nn.Sequential(
            torch.nn.Conv2d(259, 256, kernel_size=3),
            torch.nn.Sigmoid(),
        )

    def forward(self, img: torch.Tensor) -> torch.Tensor:
        """Apply the function on the images.

        Parameters
        ----------
        img : torch.Tensor
            The float image batch of shape (n, 3, h, w).
            With h and w >= 192 + k*32, k positive integer.

        Returns
        -------
        lat : torch.Tensor
            The projection of the image in the latent space.
            New shape is (n, 256, (h-160)/32, (w-160)/32) with value in [0, 1].

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.nn.model.compression.img_cgavaenn import VariationalEncoder
        >>> encoder = VariationalEncoder()
        >>> encoder(torch.rand((10, 3, 192, 192+2*32))).shape
        torch.Size([10, 256, 1, 3])
        >>>
        """
        assert isinstance(img, torch.Tensor), img.__class__.__name__
        assert img.ndim == 4, img.shape
        assert img.shape[1] == 3, img.shape
        assert img.shape[2:] >= (192, 192), img.shape
        assert img.shape[2] % 32 == 0, img.shape
        assert img.shape[3] % 32 == 0, img.shape
        assert img.dtype.is_floating_point, img.dtype

        mean = (
            torch.mean(img, dim=(2, 3), keepdim=True)
            .expand(-1, 3, img.shape[2]//32-3, img.shape[3]//32-3)
        )
        x = self.pre(img)
        x = self.encoder(x)
        lat = self.post(torch.cat((x, mean), dim=1))
        if self.training:
            lat = self.add_quantization_noise(lat)
        return lat

    @staticmethod
    def add_quantization_noise(lat: torch.Tensor) -> torch.Tensor:
        """Add a uniform noise in order to simulate the quantization into uint8.

        Parameters
        ----------
        lat : torch.Tensor
            The float lattent space of shape (n, 256, a, b) with value in range ]0, 1[.

        Returns
        -------
        noised_lat : torch.Tensor
            The input tensor with a aditive uniform noise U(-.5/255, .5/255).
            The finals values are clamped to stay in the range [0, 1].

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.nn.model.compression.img_cgavaenn import VariationalEncoder
        >>> lat = torch.rand((10, 256, 1, 3))
        >>> q_lat = VariationalEncoder.add_quantization_noise(lat)
        >>> torch.all(abs(q_lat - lat) <= 0.5/255)
        tensor(True)
        >>> abs((q_lat - lat).mean().round(decimals=4))
        tensor(0.)
        >>>
        """
        assert isinstance(lat, torch.Tensor), lat.__class__.__name__
        assert lat.ndim == 4, lat.shape
        assert lat.shape[1] == 256, lat.shape
        assert lat.dtype.is_floating_point, lat.dtype

        noise = torch.rand_like(lat)/255
        noise -= 0.5/255
        out = lat + noise
        out = torch.clamp(out, min=0, max=1)
        return out


class Decoder(torch.nn.Module):
    """Unfold the projected encoded images into the color space."""

    def __init__(self):
        super().__init__()

        eta = 1.605

        self.pre = torch.nn.Sequential(
            torch.nn.ConstantPad2d(2, 0.5),
            torch.nn.Conv2d(258, 256, kernel_size=1),
            torch.nn.ReLU(inplace=True),
        )
        self.decoder = torch.nn.Sequential(
            *(
                torch.nn.Sequential(
                    torch.nn.ConvTranspose2d(
                        round(24*eta**layer),
                        round(24*eta**(layer-1)),
                        kernel_size=4,
                        stride=2,
                        padding=1,
                        bias=False,
                    ),
                    torch.nn.BatchNorm2d(round(24*eta**(layer-1))),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.Dropout(0.1),
                    torch.nn.Conv2d(
                        round(24*eta**(layer-1)),
                        round(24*eta**(layer-1)),
                        kernel_size=3,
                        stride=1,
                        padding=2,
                    ),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.Dropout(0.1),
                )
                for layer in range(5, 0, -1)
            ),
        )
        self.head_mse = torch.nn.Sequential(
            torch.nn.Conv2d(24, 12, kernel_size=5),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(12, 3, kernel_size=5),
            torch.nn.Sigmoid(),
        )
        self.head_gen = torch.nn.Sequential(
            torch.nn.Conv2d(24, 24, kernel_size=3, bias=False),
            torch.nn.BatchNorm2d(24),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(24, 24, kernel_size=3),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(24, 17, kernel_size=3, bias=False),
            torch.nn.BatchNorm2d(17),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(17, 17, kernel_size=3),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(17, 10, kernel_size=3, bias=False),
            torch.nn.BatchNorm2d(10),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(10, 10, kernel_size=3),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(10, 5, kernel_size=3),
            torch.nn.ELU(),
            torch.nn.Conv2d(5, 3, kernel_size=3),
            torch.nn.Sigmoid(),
        )

    def forward(self, lat: torch.Tensor, *, mse: bool = True, gen: bool = True) -> torch.Tensor:
        """Apply the function on the latent images.

        Parameters
        ----------
        lat : torch.Tensor
            The projected image in the latent space of shape (n, 256, hl, wl).
        mse : boolean, default=True
            If True, return the mse head result at first position, return None otherwise.
        gen : boolean, default=True
            If True, return the generative head result at second position, return None otherwise.

        Returns
        -------
        img_mse : torch.Tensor or None
            A close image in colorspace to the input image.
            It is as mutch bijective as possible than VariationalEncoder.
            New shape is (n, 256, 160+hl*32, 160+wl*32) with value in [0, 1].
        img_gen : torch.Tensor or None
            A beautifull image in colorspace, don't match very accurately to the original.
            It can be extrapolated in order to reinvent details.
            New shape is (n, 256, 160+hl*32, 160+wl*32) with value in [0, 1].

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.nn.model.compression.img_cgavaenn import Decoder
        >>> decoder = Decoder()
        >>> mse, gen = decoder(torch.rand((10, 256, 1, 3)))
        >>> mse.shape
        torch.Size([10, 3, 192, 256])
        >>> gen.shape
        torch.Size([10, 3, 192, 256])
        >>>
        """
        assert isinstance(lat, torch.Tensor), lat.__class__.__name__
        assert lat.ndim == 4, lat.shape
        assert lat.shape[1] == 256, lat.shape
        assert lat.shape[2:] >= (1, 1), lat.shape
        assert lat.dtype.is_floating_point, lat.dtype
        assert isinstance(mse, bool), mse.__class__.__name__
        assert isinstance(gen, bool), gen.__class__.__name__
        assert mse or gen, "at least one head has to be computed"

        pos_h = torch.linspace(-1, 1, lat.shape[2], dtype=lat.dtype, device=lat.device)
        pos_w = torch.linspace(-1, 1, lat.shape[3], dtype=lat.dtype, device=lat.device)
        pos_h, pos_w = pos_h.reshape(1, 1, -1, 1), pos_w.reshape(1, 1, 1, -1)
        pos_h, pos_w = (
            pos_h.expand(len(lat), 1, *lat.shape[2:]),
            pos_w.expand(len(lat), 1, *lat.shape[2:]),
        )

        x = self.pre(torch.cat((lat, pos_h, pos_w), dim=1))
        x = self.decoder(x)
        mse_data = self.head_mse(x[:, :, 11:-11, 11:-11]) if mse else None
        gen_data = self.head_gen(x[:, :, 7:-7, 7:-7]) if gen else None
        return mse_data, gen_data


class Discriminator(torch.nn.Module):
    """Classify the real and generated images."""

    def __init__(self):
        super().__init__()

        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(3, 32, kernel_size=5, padding=1),
            torch.nn.LeakyReLU(0.2, inplace=True),
            torch.nn.Conv2d(32, 32, kernel_size=3, bias=False),
            torch.nn.MaxPool2d(2),
            torch.nn.BatchNorm2d(32),
            torch.nn.LeakyReLU(0.2, inplace=True),

            torch.nn.Conv2d(32, 48, kernel_size=3, padding=1),
            torch.nn.LeakyReLU(0.2, inplace=True),
            torch.nn.Conv2d(48, 48, kernel_size=3, bias=False),
            torch.nn.MaxPool2d(2),
            torch.nn.BatchNorm2d(48),
            torch.nn.LeakyReLU(0.2, inplace=True),

            torch.nn.Conv2d(48, 64, kernel_size=3, padding=1),
            torch.nn.LeakyReLU(0.2, inplace=True),
            torch.nn.Conv2d(64, 64, kernel_size=3, bias=False),
            torch.nn.MaxPool2d(2),
            torch.nn.BatchNorm2d(64),
            torch.nn.LeakyReLU(0.2, inplace=True),

            torch.nn.Conv2d(64, 96, kernel_size=3, padding=1),
            torch.nn.LeakyReLU(0.2, inplace=True),
            torch.nn.Conv2d(96, 96, kernel_size=3, bias=False),
            torch.nn.MaxPool2d(2),
            torch.nn.BatchNorm2d(96),
            torch.nn.LeakyReLU(0.2, inplace=True),

            torch.nn.Conv2d(96, 128, kernel_size=3),
            torch.nn.LeakyReLU(0.2, inplace=True),
            torch.nn.Conv2d(128, 128, kernel_size=3),
            torch.nn.MaxPool2d(2),
            torch.nn.LeakyReLU(0.2, inplace=True),

            torch.nn.Conv2d(128, 1, kernel_size=3),
            torch.nn.Sigmoid(),
        )

    def forward(self, img: torch.Tensor) -> torch.Tensor:
        """Find if the image if a fake or a real image.

        Parameters
        ----------
        img : torch.Tensor
            The float image batch of shape (n, 3, h, w).
            With h and w >= 192 + k*32, k positive integer.

        Returns
        -------
        is_fake : torch.Tensor
            A scalar in [0, 1], 0 if the image is real, 1 if it is a fake.
            New shape is (n, 1, (h-160)/32, (w-160)/32)

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.nn.model.compression.img_cgavaenn import Discriminator
        >>> discriminator = Discriminator()
        >>> discriminator(torch.rand((10, 3, 192, 192+2*32))).shape
        torch.Size([10, 1, 1, 3])
        >>>
        """
        assert isinstance(img, torch.Tensor), img.__class__.__name__
        assert img.ndim == 4, img.shape
        assert img.shape[1] == 3, img.shape
        assert img.shape[2:] >= (192, 192), img.shape
        assert img.shape[2] % 32 == 0, img.shape
        assert img.shape[3] % 32 == 0, img.shape
        assert img.dtype.is_floating_point, img.dtype

        is_fake = self.conv(img)
        return is_fake


class GAVAECNN(lightning.LightningModule):
    """Convolutive generative adversarial variational auto-encoder neuronal network."""

    def __init__(self, encoder: VariationalEncoder, decoder: Decoder, discriminator: Discriminator):
        assert isinstance(encoder, VariationalEncoder), encoder.__class__.__name__
        assert isinstance(decoder, Decoder), decoder.__class__.__name__
        assert isinstance(discriminator, Discriminator), discriminator.__class__.__name__
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.discriminator = discriminator

    # def training_step(self, batch, batch_idx):
    #     """Compute the training loss."""
    #     print(batch.shape)
    #     print(batch_idx)
    #     # return loss
