import timm
from .base_model import BaseModel

class NanoViT(BaseModel):
    def __init__(
        self,
        img_size=32,
        in_channels=3,
        num_classes=10,
    ):
        super().__init__()
        # Even smaller configuration
        self.model = timm.create_model(
            'vit_base_patch16_224',
            img_size=img_size,
            patch_size=1,
            in_chans=in_channels,
            num_classes=num_classes,
            embed_dim=32,  # Extremely small embedding dimension
            depth=3,       # Only 3 transformer layers
            num_heads=2,   # Only 2 attention heads
            mlp_ratio=2.,  # Smaller MLP ratio
            drop_rate=0.1,
            pretrained=False
        )
    
    def forward(self, x):
        return self.model(x)
        
    @property
    def config(self):
        return {
            'name': 'NanoViT-p1',
            'embed_dim': self.model.embed_dim,
            'depth': len(self.model.blocks),
            'num_heads': self.model.blocks[0].attn.num_heads,
            'num_params': sum(p.numel() for p in self.parameters())
        }