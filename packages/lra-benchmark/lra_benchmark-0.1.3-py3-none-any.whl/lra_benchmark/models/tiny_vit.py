import timm
from lra_benchmark.models.base_model import BaseModel

class TinyViT(BaseModel):
    def __init__(
        self,
        img_size=32,
        num_classes=10,
    ):
        super().__init__()
        # Using smallest possible configuration with patch_size=1
        self.model = timm.create_model(
            'vit_base_patch16_224',
            img_size=img_size,
            patch_size=1,
            in_chans=1,
            num_classes=num_classes,
            embed_dim=64,
            depth=4,
            num_heads=2,
            mlp_ratio=2.,
            drop_rate=0.1,
            pretrained=False
        )
    
    def forward(self, x):
        return self.model(x)
        
    @property
    def config(self):
        return {
            'name': 'TinyViT-p1',
            'embed_dim': self.model.embed_dim,
            'depth': len(self.model.blocks),
            'num_heads': self.model.blocks[0].attn.num_heads,
            'num_params': sum(p.numel() for p in self.parameters())
        }
        