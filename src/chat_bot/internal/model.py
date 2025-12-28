import torch.nn as nn

class IntentModel(nn.Module):
    def __init__(self, input_dim: int, num_classes: int):
        super().__init__()
        self.input_layer = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.SiLU()
        )
        self.res_block = nn.Sequential(
            nn.Linear(256, 256),
            nn.BatchNorm1d(256),
            nn.SiLU(),
            nn.Dropout(0.4),
            nn.Linear(256, 256),
            nn.BatchNorm1d(256)
        )
        self.post_res_activation = nn.SiLU()
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.SiLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
        x = self.input_layer(x)
        residual = x
        x = self.res_block(x)
        x += residual
        x = self.post_res_activation(x)
        return self.classifier(x)
